from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re


# log_parser.py가 저장된 폴더를 기준으로 파일 경로를 설정합니다.
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_dco_log.txt"
OUTPUT_FILE = BASE_DIR / "incident_summary.md"

# 핵심적으로 확인할 이벤트 목록입니다.
IMPORTANT_EVENTS = ("CRC_ERROR", "LINK_DOWN", "TICKET_ESCALATED")

# 이상 로그로 분류할 심각도입니다.
ALERT_SEVERITIES = {"WARNING", "ERROR", "CRITICAL"}


def normalize_event(event):
    """
    이벤트 이름의 공백, 밑줄, 대소문자 차이를 통일합니다.
    예: Link Down -> LINK_DOWN
    """

    normalized = re.sub(r"[_\s]+", " ", event.strip().upper())

    # 'CRC error 증가'처럼 뒤에 다른 문자가 있어도 CRC_ERROR로 처리합니다.
    if normalized.startswith("CRC ERROR"):
        return "CRC_ERROR"

    event_mapping = {
        "NORMAL HEARTBEAT": "NORMAL_HEARTBEAT",
        "FAN ALERT": "FAN_ALERT",
        "TEMPERATURE WARNING": "TEMPERATURE_WARNING",
        "SSD FAILURE WARNING": "SSD_FAILURE_WARNING",
        "LINK DOWN": "LINK_DOWN",
        "LINK UP": "LINK_UP",
        "TICKET OPENED": "TICKET_OPENED",
        "TICKET ESCALATED": "TICKET_ESCALATED",
        "MAINTENANCE COMPLETED": "MAINTENANCE_COMPLETED",
    }

    return event_mapping.get(normalized, normalized.replace(" ", "_"))


def remove_ip_address(message):
    """
    메시지에 포함된 IPv4 형태의 문자열을 보고서에서 가립니다.
    """

    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    cleaned_message = re.sub(ip_pattern, "[IP_REMOVED]", message)

    # Markdown 표가 깨지지 않도록 | 문자를 처리합니다.
    return cleaned_message.replace("|", r"\|")


def main():
    if not INPUT_FILE.exists():
        print(f"오류: 로그 파일을 찾을 수 없습니다: {INPUT_FILE}")
        return

    logs = []
    format_errors = []
    total_lines = 0

    severity_counts = Counter()
    event_counts = Counter()

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            # 빈 줄은 분석하지 않습니다.
            if not line:
                continue

            total_lines += 1

            # | 문자를 기준으로 최대 5개 항목으로 나눕니다.
            parts = [part.strip() for part in line.split("|", 4)]

            if len(parts) != 5:
                format_errors.append(
                    f"{line_number}번째 줄: 항목이 5개가 아닙니다."
                )
                continue

            timestamp, device, severity, event, message = parts

            severity = severity.upper()
            event = normalize_event(event)
            message = remove_ip_address(message)

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

    # WARNING, ERROR, CRITICAL 로그를 분류합니다.
    alert_logs = [
        log for log in logs
        if log["severity"] in ALERT_SEVERITIES
    ]

    # 핵심 이벤트는 심각도와 관계없이 이벤트 이름을 기준으로 찾습니다.
    important_logs = [
        log for log in logs
        if log["event"] in IMPORTANT_EVENTS
    ]

    severity_descriptions = {
        "INFO": "정상 상태 또는 일반 운영 기록",
        "WARNING": "이상 징후가 감지되어 확인이 필요한 기록",
        "ERROR": "오류가 발생하여 추가 확인이 필요한 기록",
        "CRITICAL": "우선 확인과 에스컬레이션 검토가 필요한 기록",
    }

    result = [
        "# 📊 DCO 로그 분석 보고서",
        "",
        "이 보고서는 교육용 샘플 DCO 로그 파일인 "
        "`sample_dco_log.txt`를 Python으로 분석하여 자동 생성한 결과입니다.",
        "",
        "## 📈 1. 전체 통계",
        "",
        f"- **분석된 총 로그 라인 수:** {total_lines}개",
        f"- **정상적으로 분석된 로그:** {len(logs)}개",
        f"- **형식 오류가 발생한 로그:** {len(format_errors)}개",
        "",
        "---",
        "",
        "## ⚠️ 2. 심각도별 로그 분포",
        "",
        "| 심각도 | 로그 수 | 진단 상태 및 비고 |",
        "| --- | ---: | --- |",
    ]

    for severity in ("INFO", "WARNING", "ERROR", "CRITICAL"):
        result.append(
            f"| {severity} | {severity_counts[severity]} | "
            f"{severity_descriptions[severity]} |"
        )

    result.extend([
        "",
        "---",
        "",
        "## 🔍 3. 이벤트별 발생 빈도",
        "",
        "| 이벤트명 | 발생 횟수 |",
        "| --- | ---: |",
    ])

    # 발생 횟수가 많은 이벤트부터 표시합니다.
    sorted_events = sorted(
        event_counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    for event, count in sorted_events:
        result.append(f"| {event} | {count} |")

    result.extend([
        "",
        "---",
        "",
        "## 🚨 4. 경고·오류·심각 로그 목록",
        "",
        "| 발생 일시 | 장비명 | 심각도 | 이벤트명 | 상세 메시지 |",
        "| --- | --- | ---: | --- | --- |",
    ])

    if alert_logs:
        for log in alert_logs:
            result.append(
                f"| {log['timestamp']} | {log['device']} | "
                f"`{log['severity']}` | {log['event']} | "
                f"{log['message']} |"
            )
    else:
        result.append(
            "| - | - | - | - | 해당 로그가 없습니다. |"
        )

    result.extend([
        "",
        "---",
        "",
        "## 🎯 5. 장애 핵심 감지 요약",
        "",
        "| 감지 유형 | 발생 일시 | 장비명 | 심각도 | 메시지 |",
        "| --- | --- | --- | ---: | --- |",
    ])

    if important_logs:
        for log in important_logs:
            result.append(
                f"| {log['event']} | {log['timestamp']} | "
                f"{log['device']} | `{log['severity']}` | "
                f"{log['message']} |"
            )
    else:
        result.append(
            "| - | - | - | - | 핵심 이벤트가 발견되지 않았습니다. |"
        )

    result.extend([
        "",
        "---",
        "",
        "## 📝 6. 형식 오류 및 확인 메모",
        "",
    ])

    if format_errors:
        result.append("### 형식 오류")
        result.append("")

        for error in format_errors:
            result.append(f"- {error}")
    else:
        result.append("- 형식 오류가 없습니다.")

    result.extend([
        "- SAMPLE, DEMO, EDU 접두어가 붙은 교육용 장비명만 사용했습니다.",
        "- IP 주소 형태의 문자열은 `[IP_REMOVED]`로 처리했습니다.",
        "- 로그만으로 실제 장애 원인을 확정하지 않았습니다.",
        "",
    ])

    # 외부 패키지 없이 UTC+9 기준으로 KST 시각을 생성합니다.
    kst = timezone(timedelta(hours=9))
    generated_at = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

    result.extend([
        "---",
        "",
        f"- **보고서 생성 시각:** {generated_at} (KST)",
        "- 본 보고서는 교육용 시뮬레이션 결과이며 "
        "실제 인프라 운영 데이터가 아닙니다.",
    ])

    OUTPUT_FILE.write_text("\n".join(result), encoding="utf-8")

    print(f"분석 완료: {OUTPUT_FILE}")
    print(f"전체 로그: {total_lines}개")
    print(f"정상 분석: {len(logs)}개")
    print(f"형식 오류: {len(format_errors)}개")


if __name__ == "__main__":
    main()