# Frontend Display Spec

## 목적
백엔드에서 받은 Youth-Sync answer JSON을 사용자가 이해하기 쉬운 카드 형태로 표시한다.

## 표시 영역

| 영역 | JSON key | 표시 방식 |
|---|---|---|
| 판정 상태 | result_status | 상단 배지 |
| 사용자 조건 | profile_used | 요약 박스 |
| 추가 확인 필요 | need_more_info | 체크리스트 |
| 추천 정책 | recommended_policies | 카드 목록 |
| 주거 근거 | retrieved_chunks | 근거 카드 |
| 주의사항 | caution_notes | 안내 박스 |
| 출처 | citations | 링크 목록 |
| 다음 행동 | next_action | 하단 강조 문장 |

## 숨길 항목
- debug는 최종 사용자 화면에 노출하지 않는다.

## 주거 질문 표시 규칙
recommended_policies가 비어 있어도 retrieved_chunks가 있으면 정상 결과로 본다.

## 취업 질문 표시 규칙
recommended_policies가 1개 이상이면 정책 카드로 표시한다.

## 빈 결과 처리
추천 정책과 retrieved_chunks가 모두 없으면:
“현재 조건으로는 후보를 찾지 못했습니다. 추가 정보를 입력해 주세요.”를 표시한다.