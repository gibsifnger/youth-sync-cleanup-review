# Youth-Sync Demo Questions

## 시연 질문 1
서울 사는 27세 무주택 구직자인데 월세 지원 받을 수 있을까?

기대 결과:
- 주거 질문으로 분류
- result_status: 확인 필요
- need_more_info: 소득수준, 세대주 여부
- retrieved_chunks 표시
- recommended_policies는 0개여도 정상

---

## 시연 질문 2
경기도 거주 25세 중소기업 재직자인데 취업 지원 정책이 있을까?

기대 결과:
- 취업 질문으로 분류
- recommended_policies 표시
- citations 표시
- need_more_info: 소득수준

---

## 시연 질문 3
올해 퇴사한 28세 자취생인데 월세가 부담돼

기대 결과:
- 퇴사: unemployed
- 자취: renting
- 월세/주거 질문으로 분류
- 지역은 unknown
- retrieved_chunks 표시

---

## 시연 질문 4
무주택인데 세대주는 아니야. 주거 지원이 가능해?

기대 결과:
- housing_status: homeless
- household_head_status: no
- age, region은 unknown
- need_more_info 표시
- retrieved_chunks 표시

---

## 시연 질문 5
서울 거주 31세 직장인인데 청년 정책 대상이 아직 되나

기대 결과:
- age: 31
- region: 서울
- employment_status: employed
- interest_tags가 비어 있을 수 있음
- 추천 범위가 넓어질 수 있으므로 한계 설명용