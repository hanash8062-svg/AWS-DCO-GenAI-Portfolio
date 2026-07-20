from collections import Counter
from pathlib import Path

# 현재 Python 파일이 있는 폴더를 기준으로 경로를 설정합니다.
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_dco_log.txt"
OUTPUT_FILE = BASE_DIR / "incident_summary.md"

IMPORTANT_EVENTS = {"CRC_ERROR", "LINK_DOWN", "TICKET_ESCALATED"}


def main():
    if not INPUT_FILE.exists():
        print(f"오류: 로그 파일을 찾을 수 없습니다: {INPUT_FILE}")
        return

    total_lines = 0
    logs = []
    format_errors = []

    severity_counts = Counter()
    event_counts = Counter()

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line:
                continue

            total_lines += 1

            parts = [part.strip() for part in line.split("|", 4)]

            if len(parts) != 5:
                format_errors.append(f"{line_number}번째 줄: 형식 오류")
                continue

            timestamp, device, severity, event, message = parts

            severity = severity.upper()
            event = event.upper()

            log = {
                "timestamp": timestamp,
                "device": device,
                "severity": severity,
                "event": event,
                "message": message,
            }

            logs.append(log)
            severity_counts[severity] += 1
            event_counts[event] += 1

    warning_critical_logs = [
        log
        for log in logs
        if log["severity"] in {"WARNING", "CRITICAL"}
    ]

    important_logs = [
        log
        for log in logs
        if log["event"] in IMPORTANT_EVENTS
    ]

    result = [
        "# DCO 교육용 샘플 로그 분석 결과",
        "",
        "## 1. 기본 정보",
        f"- 전체 로그 줄 수: **{total_lines}**",
        f"- 정상 분석 줄 수: **{len(logs)}**",
        f"- 형식 오류 줄 수: **{len(format_errors)}**",
        "",
        "## 2. 심각도별 개수",
        "",
        "| 심각도 | 개수 |",
        "| --- | ---: |",
        f"| INFO | {severity_counts['INFO']} |",
        f"| WARNING | {severity_counts['WARNING']} |",
        f"| CRITICAL | {severity_counts['CRITICAL']} |",
        "",
        "## 3. 이벤트별 개수",
        "",
        "| 이벤트 | 개수 |",
        "| --- | ---: |",
    ]

    for event, count in sorted(event_counts.items()):
        result.append(f"| {event} | {count} |")

    result.extend([
        "",
        "## 4. WARNING 또는 CRITICAL 로그",
        "",
    ])

    if warning_critical_logs:
        for log in warning_critical_logs:
            result.append(
                f"- {log['timestamp']} | "
                f"{log['device']} | "
                f"{log['severity']} | "
                f"{log['event']} | "
                f"{log['message']}"
            )
    else:
        result.append("- 해당 로그가 없습니다.")

    result.extend([
        "",
        "## 5. 주요 이벤트 요약",
        "",
    ])

    for event in ("CRC_ERROR", "LINK_DOWN", "TICKET_ESCALATED"):
        matching_logs = [
            log for log in important_logs
            if log["event"] == event
        ]

        result.append(f"### {event}: {len(matching_logs)}건")

        if matching_logs:
            for log in matching_logs:
                result.append(
                    f"- {log['timestamp']} / "
                    f"{log['device']} / "
                    f"{log['severity']} / "
                    f"{log['message']}"
                )
        else:
            result.append("- 해당 이벤트가 없습니다.")

        result.append("")

    result.extend([
        "## 6. 형식 오류",
        "",
    ])

    if format_errors:
        for error in format_errors:
            result.append(f"- {error}")
    else:
        result.append("- 형식 오류가 없습니다.")

    result.extend([
        "",
        "## 7. 확인 메모",
        "",
        "- SAMPLE, DEMO, EDU 장비명으로 작성된 교육용 로그입니다.",
        "- 로그만으로 실제 장애 원인을 단정하지 않았습니다.",
    ])

    OUTPUT_FILE.write_text("\n".join(result), encoding="utf-8")

    print(f"분석 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    