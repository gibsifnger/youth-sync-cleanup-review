# Day4 Integration Status

## 현재 완료된 것
- A 정책 메타데이터 연결 완료
- B 주거 chunk handover 연결 완료
- C profile parser 완료
- D answer pipeline 완료
- 10개 예상질문 테스트 완료

## 현재 흐름
사용자 질문
→ C_profile/profile_parser_final.py
→ D_retrieval/rag_pipeline.py
→ A_policy_handover_v2/policy_master_final.csv
→ B_chunks_handover_v1/housing_chunks_final.jsonl
→ answer JSON 반환

## 백엔드 연결 방식
입력:
{
  "raw_text": "서울 사는 27세 무주택 구직자인데 월세 지원 받을 수 있을까?"
}

처리:
1. parse_profile(raw_text)
2. generate_answer(profile)
3. answer JSON 반환

## 현재 한계
- A 데이터가 취업 정책 중심이라 주거 정책 추천은 0개일 수 있음
- 주거 질문은 B handover chunk로 확인 필요 정보를 제공함
- B chunk는 Day4 통합 테스트용 handover_stub임
- 최종 신청 가능 여부는 확인 필요로 유지함