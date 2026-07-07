# 8차시 로그 장애 진단 검증 기록

## 1. 실습 개요

- 실습명: agy와 협업해 다중 서버 로그 장애 진단
- 작성자: 한성호
- 분석 대상 파일:
  - server01.log
  - server02.log
  - server03.log
  - server04.log
- 분석 이벤트:
  - CRC error
  - Link Down
- 사용 도구:
  - agy
  - Python
  - grep 또는 PowerShell Select-String

---

## 2. 1차 요청 프롬프트

```text
server*.log 파일들을 읽어서 CRC error와 Link Down이 각각 몇 번 나오는지
서버별로 세는 파이썬 스크립트를 만들어서 실행해줘.
```

---

## 3. 1차 결과: 단순 문자열 기준 예시

아래 값은 단순히 대소문자를 엄격히 보거나 문자열만 세었을 때 나올 수 있는 1차 결과 예시입니다.
실제 agy 1차 결과가 다르면 본인의 1차 실행값으로 바꿔 적으면 됩니다.

| 서버 | CRC error | Link Down |
|---|---:|---:|
| server01 | 17 | 4 |
| server02 | 20 | 7 |
| server03 | 26 | 5 |
| server04 | 24 | 6 |
| **합계** | **87** | **22** |

---

## 4. 교차검증 결과: grep -i 기준

`grep -i "crc error"`는 대소문자 문제는 해결하지만, `CRC error recovered` 또는 `no CRC error found` 같은 INFO 문장까지 세기 때문에 CRC error 검증값이 과대 계산됩니다.
`grep -i "link down"`은 이 로그에서는 최종값과 일치했습니다.

| 서버 | CRC error | Link Down |
|---|---:|---:|
| server01 | 35 | 11 |
| server02 | 31 | 19 |
| server03 | 47 | 8 |
| server04 | 34 | 22 |
| **합계** | **147** | **60** |

---

## 5. 더 정확한 교차검증 명령어

### Git Bash / WSL / macOS / Linux

```bash
grep -i "ERROR.*crc error" server01.log | wc -l
grep -i "ERROR.*link down" server01.log | wc -l
```

### Windows PowerShell

```powershell
(Select-String -Path .\server01.log -Pattern "ERROR.*crc error").Count
(Select-String -Path .\server01.log -Pattern "ERROR.*link down").Count
```

server02.log, server03.log, server04.log에도 같은 방식으로 적용합니다.

---

## 6. 1차 결과와 검증 결과가 달랐던 이유

1차 스크립트는 다음 함정을 놓칠 수 있었습니다.

1. 대소문자 차이: `CRC ERROR`, `CRC Error`, `crc error`, `LINK DOWN`, `Link down` 등이 섞여 있음
2. 멀티라인 로그: ERROR 한 건이 다음 줄의 상세 설명과 함께 기록됨
3. 정상/복구 문장: `CRC error recovered`, `interface up, no CRC error found`는 실제 장애가 아닌데 단순 검색에서는 집계될 수 있음
4. 따라서 최종 스크립트는 `ERROR` 레벨 로그 중에서만 `CRC error`, `Link Down`을 집계하도록 수정함

---

## 7. 재요청 프롬프트

```text
아까 스크립트는 단순 문자열 검색이라 일부를 놓치거나 잘못 세고 있습니다.

수정 조건:
1. 대소문자를 무시하고 CRC error, CRC ERROR, Crc Error, crc error를 같은 이벤트로 세어 주세요.
2. Link Down도 LINK DOWN, Link down, link down을 모두 같은 이벤트로 세어 주세요.
3. 여러 줄에 걸쳐 기록된 ERROR 상세 설명은 하나의 이벤트로 묶어 주세요.
4. 단, CRC error recovered, no CRC error found, CRCcheck OK처럼 오류가 없거나 복구되었다는 INFO 문장은 실제 CRC error로 세지 마세요.
5. 실제 장애 이벤트는 ERROR 레벨 로그만 기준으로 세어 주세요.
6. server01.log~server04.log를 각각 분석하고 서버별 개수와 전체 합계를 출력해 주세요.
7. 최종 스크립트를 07_log_analysis_script2/log_analyzer.py로 저장해 주세요.
```

---

## 8. 2차 최종 결과: ERROR 레벨 기준

| 서버 | CRC error | Link Down |
|---|---:|---:|
| server01 | 23 | 11 |
| server02 | 17 | 19 |
| server03 | 31 | 8 |
| server04 | 14 | 22 |
| **합계** | **85** | **60** |

---

## 9. 최종 판단

2차 수정 스크립트에서는 대소문자 차이, 멀티라인 로그, 정상/복구 문장 오탐 문제를 반영했습니다.
최종 결과는 수업에서 제시된 기준값과 일치합니다.

---

## 10. 보안 확인 메모

- 실제 AWS 내부 로그를 사용하지 않았습니다.
- 실제 계정정보, 토큰, API 키를 입력하지 않았습니다.
- 실제 장비 점검 명령이나 외부 대상 접속 명령을 실행하지 않았습니다.
- 첨부된 교육용 로그 파일만 분석했습니다.
