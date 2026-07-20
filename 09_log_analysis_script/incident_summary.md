# DCO 교육용 샘플 로그 분석 결과

## 1. 기본 정보
- 전체 로그 줄 수: **12**
- 정상 분석 줄 수: **12**
- 형식 오류 줄 수: **0**

## 2. 심각도별 개수

| 심각도 | 개수 |
| --- | ---: |
| INFO | 6 |
| WARNING | 4 |
| CRITICAL | 2 |

## 3. 이벤트별 개수

| 이벤트 | 개수 |
| --- | ---: |
| CRC_ERROR | 2 |
| HEALTH_CHECK | 1 |
| LINK_DOWN | 1 |
| LINK_UP | 2 |
| POWER_ALERT | 1 |
| POWER_NORMAL | 1 |
| TEMP_WARNING | 1 |
| TICKET_CLOSED | 1 |
| TICKET_CREATED | 1 |
| TICKET_ESCALATED | 1 |

## 4. WARNING 또는 CRITICAL 로그

- 2026-01-20 09:03:15 | SAMPLE_TOR_SW_01 | WARNING | CRC_ERROR | CRC error detected on sample interface
- 2026-01-20 09:05:40 | SAMPLE_TOR_SW_01 | WARNING | CRC_ERROR | Repeated CRC error observed on sample interface
- 2026-01-20 09:07:10 | SAMPLE_TOR_SW_01 | CRITICAL | LINK_DOWN | Link Down observed on sample interface
- 2026-01-20 09:10:00 | DEMO_SERVER_01 | WARNING | TEMP_WARNING | Sample temperature warning recorded
- 2026-01-20 09:12:30 | SAMPLE_TOR_SW_01 | CRITICAL | TICKET_ESCALATED | Educational ticket escalated for instructor review
- 2026-01-20 09:20:45 | EDU_PDU_01 | WARNING | POWER_ALERT | Educational power alert recorded

## 5. 주요 이벤트 요약

### CRC_ERROR: 2건
- 2026-01-20 09:03:15 / SAMPLE_TOR_SW_01 / WARNING / CRC error detected on sample interface
- 2026-01-20 09:05:40 / SAMPLE_TOR_SW_01 / WARNING / Repeated CRC error observed on sample interface

### LINK_DOWN: 1건
- 2026-01-20 09:07:10 / SAMPLE_TOR_SW_01 / CRITICAL / Link Down observed on sample interface

### TICKET_ESCALATED: 1건
- 2026-01-20 09:12:30 / SAMPLE_TOR_SW_01 / CRITICAL / Educational ticket escalated for instructor review

## 6. 형식 오류

- 형식 오류가 없습니다.

## 7. 확인 메모

- SAMPLE, DEMO, EDU 장비명으로 작성된 교육용 로그입니다.
- 로그만으로 실제 장애 원인을 단정하지 않았습니다.