# 📊 DCO 로그 분석 보고서

이 보고서는 교육용 샘플 DCO 로그 파일인 `sample_dco_log.txt`를 Python으로 분석하여 자동 생성한 결과입니다.

## 📈 1. 전체 통계

- **분석된 총 로그 라인 수:** 140개
- **정상적으로 분석된 로그:** 140개
- **형식 오류가 발생한 로그:** 0개

---

## ⚠️ 2. 심각도별 로그 분포

| 심각도 | 로그 수 | 진단 상태 및 비고 |
| --- | ---: | --- |
| INFO | 135 | 정상 상태 또는 일반 운영 기록 |
| WARNING | 3 | 이상 징후가 감지되어 확인이 필요한 기록 |
| ERROR | 2 | 오류가 발생하여 추가 확인이 필요한 기록 |
| CRITICAL | 0 | 우선 확인과 에스컬레이션 검토가 필요한 기록 |

---

## 🔍 3. 이벤트별 발생 빈도

| 이벤트명 | 발생 횟수 |
| --- | ---: |
| NORMAL_HEARTBEAT | 125 |
| MAINTENANCE_COMPLETED | 3 |
| TICKET_ESCALATED | 3 |
| TICKET_OPENED | 3 |
| CRC_ERROR | 1 |
| FAN_ALERT | 1 |
| LINK_DOWN | 1 |
| LINK_UP | 1 |
| SSD_FAILURE_WARNING | 1 |
| TEMPERATURE_WARNING | 1 |

---

## 🚨 4. 경고·오류·심각 로그 목록

| 발생 일시 | 장비명 | 심각도 | 이벤트명 | 상세 메시지 |
| --- | --- | ---: | --- | --- |
| 2026-07-03 01:05:00 | DEMO_CORE_SW_02 | `WARNING` | FAN_ALERT | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: [IP_REMOVED] |
| 2026-07-03 02:05:00 | EDU_SRV_R04_N12 | `WARNING` | TEMPERATURE_WARNING | Chassis temperature reached 42C (Threshold: 40C). IP: [IP_REMOVED] |
| 2026-07-03 02:10:00 | EDU_SRV_R04_N12 | `ERROR` | SSD_FAILURE_WARNING | Drive Slot 3 SSD wearout indicator FAILING (SMART wear 96%). IP: [IP_REMOVED] |
| 2026-07-03 03:05:00 | SAMPLE_TOR_SW_01 | `WARNING` | CRC_ERROR | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: [IP_REMOVED] |
| 2026-07-03 03:06:00 | SAMPLE_TOR_SW_01 | `ERROR` | LINK_DOWN | Interface Gi0/1 status changed to DOWN. Connection to server lost. |

---

## 🎯 5. 장애 핵심 감지 요약

| 감지 유형 | 발생 일시 | 장비명 | 심각도 | 메시지 |
| --- | --- | --- | ---: | --- |
| TICKET_ESCALATED | 2026-07-03 01:10:00 | DEMO_CORE_SW_02 | `INFO` | Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team. |
| TICKET_ESCALATED | 2026-07-03 02:15:00 | EDU_SRV_R04_N12 | `INFO` | Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support. |
| CRC_ERROR | 2026-07-03 03:05:00 | SAMPLE_TOR_SW_01 | `WARNING` | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: [IP_REMOVED] |
| LINK_DOWN | 2026-07-03 03:06:00 | SAMPLE_TOR_SW_01 | `ERROR` | Interface Gi0/1 status changed to DOWN. Connection to server lost. |
| TICKET_ESCALATED | 2026-07-03 03:12:00 | SAMPLE_TOR_SW_01 | `INFO` | Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team. |

---

## 📝 6. 형식 오류 및 확인 메모

- 형식 오류가 없습니다.
- SAMPLE, DEMO, EDU 접두어가 붙은 교육용 장비명만 사용했습니다.
- IP 주소 형태의 문자열은 `[IP_REMOVED]`로 처리했습니다.
- 로그만으로 실제 장애 원인을 확정하지 않았습니다.

---

- **보고서 생성 시각:** 2026-07-20 12:33:37 (KST)
- 본 보고서는 교육용 시뮬레이션 결과이며 실제 인프라 운영 데이터가 아닙니다.