from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List


OUTPUT_DIR = Path("output")
HANDOVER_DIR = Path("../B_chunks_output_handover")

POLICY_OUT = HANDOVER_DIR / "housing_policy_master_from_b.csv"
CHUNK_OUT = HANDOVER_DIR / "housing_chunks_final.jsonl"
SCHEMA_REVIEW = HANDOVER_DIR / "b_output_schema_review.md"
LIMIT_NOTE = HANDOVER_DIR / "b_output_limit_note.md"


POLICY_COLUMNS = [
    "policy_id",
    "policy_name",
    "category",
    "subcategory",
    "region_scope",
    "age_min",
    "age_max",
    "employment_condition",
    "housing_condition",
    "income_condition_text",
    "apply_start_date",
    "apply_end_date",
    "apply_status",
    "source_org",
    "source_url",
    "summary",
    "source_type",
]


CHUNK_COLUMNS = [
    "chunk_id",
    "policy_id",
    "policy_name",
    "issuing_org",
    "source_doc_name",
    "source_url",
    "section_title",
    "chunk_text",
    "chunk_order",
    "has_table",
    "doc_type",
    "created_from",
]


# 홈페이지 메뉴/공통 영역이 길게 붙는 문제를 줄이기 위한 키워드
RELEVANT_MARKERS = [
    "입주자격",
    "입주 대상",
    "입주대상",
    "대상자",
    "신청자격",
    "공급대상",
    "지원대상",
    "무주택",
    "소득",
    "자산",
    "임대조건",
    "임대보증금",
    "월임대료",
    "신청방법",
    "제출서류",
    "청년",
    "대학생",
    "취업준비생",
    "신혼부부",
    "매입임대",
    "전세임대",
    "행복주택",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def short_policy_name(policy_name: str) -> str:
    """
    '청년매입임대주택 | 청년ㆍ신혼부부계층...' 같은 긴 title에서
    앞 정책명만 추출한다.
    """
    policy_name = normalize_text(policy_name)
    if "|" in policy_name:
        return policy_name.split("|")[0].strip()
    return policy_name.strip()


def crop_relevant_text(text: str, policy_name: str = "") -> str:
    """
    LH 홈페이지 전체 메뉴가 chunk_text 앞에 붙는 문제가 있어서
    정책명 또는 주거 관련 키워드가 처음 등장하는 지점부터 잘라낸다.
    """
    text = normalize_text(text)
    if not text:
        return ""

    candidates: List[int] = []

    short_name = short_policy_name(policy_name)
    if short_name and short_name in text:
        candidates.append(text.find(short_name))

    for marker in RELEVANT_MARKERS:
        idx = text.find(marker)
        if idx >= 0:
            candidates.append(idx)

    if candidates:
        start = max(min(candidates) - 80, 0)
        text = text[start:]

    # 너무 길면 D 검색/화면 표시가 흔들리므로 900자까지만 유지
    if len(text) > 900:
        text = text[:900].rstrip() + "..."

    return text


def policy_score(chunk: Dict[str, Any]) -> int:
    """
    너무 메뉴성인 chunk를 뒤로 보내기 위한 간단 점수.
    """
    text = normalize_text(chunk.get("chunk_text", ""))
    section = normalize_text(chunk.get("section_title", ""))

    score = 0

    for marker in RELEVANT_MARKERS:
        if marker in text:
            score += 2
        if marker in section:
            score += 3

    # section_title이 기타면 감점
    if section == "기타":
        score -= 2

    # 홈페이지 공통 메뉴 냄새가 강하면 감점
    menu_noise_words = [
        "통합검색",
        "새소식",
        "공지사항",
        "정보공개",
        "고객의소리",
        "부패ㆍ부조리신고",
        "공공데이터",
        "사업실명제",
    ]
    for word in menu_noise_words:
        if word in text:
            score -= 1

    return score


def read_policies() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for path in sorted(OUTPUT_DIR.glob("*_policy.json")):
        data = load_json(path)

        if not isinstance(data, dict):
            continue

        row = {}
        for col in POLICY_COLUMNS:
            value = data.get(col, "unknown")
            if value is None or value == "":
                value = "unknown"
            row[col] = value

        # B 원본 출처임을 명확히 표시
        if row.get("source_type") in ("unknown", "", None):
            row["source_type"] = "lh_web"

        rows.append(row)

    return rows


def read_and_clean_chunks() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for path in sorted(OUTPUT_DIR.glob("*_chunks.json")):
        data = load_json(path)

        if isinstance(data, dict):
            chunks = data.get("chunks", [])
        elif isinstance(data, list):
            chunks = data
        else:
            chunks = []

        if not isinstance(chunks, list):
            continue

        # 정책별 chunk 중 점수가 너무 낮은 것만 남기면 전부 날아갈 수 있으므로
        # 우선 전부 읽되, 정렬 후 정책당 상위 5개까지만 사용한다.
        cleaned_for_policy: List[Dict[str, Any]] = []

        for raw_chunk in chunks:
            if not isinstance(raw_chunk, dict):
                continue

            chunk = {}
            for col in CHUNK_COLUMNS:
                value = raw_chunk.get(col, "unknown")
                if value is None or value == "":
                    value = "unknown"
                chunk[col] = value

            policy_name = normalize_text(chunk.get("policy_name", ""))
            chunk["policy_name"] = policy_name
            chunk["source_doc_name"] = normalize_text(chunk.get("source_doc_name", ""))
            chunk["section_title"] = normalize_text(chunk.get("section_title", "기타"))
            chunk["chunk_text"] = crop_relevant_text(chunk.get("chunk_text", ""), policy_name=policy_name)

            if not chunk["chunk_text"]:
                continue

            chunk["_score"] = policy_score(chunk)
            cleaned_for_policy.append(chunk)

        cleaned_for_policy.sort(key=lambda x: x.get("_score", 0), reverse=True)

        # 정책당 최대 5개 chunk만 전달
        for chunk in cleaned_for_policy[:5]:
            chunk.pop("_score", None)
            rows.append(chunk)

    return rows


def write_policy_csv(rows: List[Dict[str, Any]]) -> None:
    with POLICY_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=POLICY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_chunk_jsonl(rows: List[Dict[str, Any]]) -> None:
    with CHUNK_OUT.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_docs(policy_count: int, chunk_count: int) -> None:
    SCHEMA_REVIEW.write_text(
        f"""# B output schema review

## 확인 결과
- B 원본 output의 `*_policy.json`은 5-1 정책 스키마 key를 대부분 충족합니다.
- B 원본 output의 `*_chunks.json`은 `{{"chunks": [...]}}` 구조입니다.
- D 연결을 위해 여러 파일을 하나의 CSV/JSONL로 병합했습니다.

## 생성 파일
- `housing_policy_master_from_b.csv`
- `housing_chunks_final.jsonl`

## 생성 개수
- 정책 row: {policy_count}
- chunk row: {chunk_count}

## 원칙
- B 원본 output은 덮어쓰지 않습니다.
- 이 폴더는 D 연결용 변환본입니다.
- 정책과 chunk는 `policy_id`로 연결합니다.
""",
        encoding="utf-8",
    )

    LIMIT_NOTE.write_text(
        """# B output handover limit note

## 현재 한계
1. B 원본 chunk에는 LH 홈페이지 메뉴/공통 문구가 일부 섞여 있습니다.
2. 본 변환 스크립트는 정책명/주거 관련 키워드 기준으로 chunk_text를 잘라 검색 품질을 보정합니다.
3. section_title이 `기타`로 들어간 chunk가 많아 문단 제목 품질은 추가 개선 여지가 있습니다.
4. apply_status는 B policy 원본 값을 따르며, 모르는 값은 `unknown`으로 둡니다.
5. 이 파일은 B 원본 산출물이 아니라 D 연결용 변환본입니다.

## 다음 작업
- D에서 A policy master + B housing policy master를 함께 읽도록 수정
- D에서 B housing_chunks_final.jsonl을 검색 대상으로 사용
- 질문 5개로 주거/취업 결과 재검수
""",
        encoding="utf-8",
    )


def main() -> None:
    HANDOVER_DIR.mkdir(exist_ok=True)

    policies = read_policies()
    chunks = read_and_clean_chunks()

    write_policy_csv(policies)
    write_chunk_jsonl(chunks)
    write_docs(policy_count=len(policies), chunk_count=len(chunks))

    print("B output handover created")
    print(f"- policies: {len(policies)} -> {POLICY_OUT}")
    print(f"- chunks:   {len(chunks)} -> {CHUNK_OUT}")
    print(f"- review:   {SCHEMA_REVIEW}")
    print(f"- limit:    {LIMIT_NOTE}")


if __name__ == "__main__":
    main()