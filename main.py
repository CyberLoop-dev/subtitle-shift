import argparse
import re
import sys
from pathlib import Path

TIMESTAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
TIMING_LINE = re.compile(r"^(\d{2}:\d{2}:\d{2},\d{3})(\s+-->\s+)(\d{2}:\d{2}:\d{2},\d{3})(.*)$")


def to_milliseconds(value):
    match = TIMESTAMP.fullmatch(value)
    if not match:
        raise ValueError(f"Invalid timestamp: {value}")
    hours, minutes, seconds, millis = map(int, match.groups())
    if minutes > 59 or seconds > 59:
        raise ValueError(f"Invalid timestamp component: {value}")
    return (((hours * 60 + minutes) * 60) + seconds) * 1000 + millis


def from_milliseconds(value):
    value = max(0, value)
    hours, remainder = divmod(value, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def validate_srt(text):
    issues = []
    previous_start = -1
    cues = 0
    for number, line in enumerate(text.splitlines(), start=1):
        if "-->" not in line:
            continue
        match = TIMING_LINE.fullmatch(line.strip())
        if not match:
            issues.append(f"line {number}: malformed timing line")
            continue
        try:
            start = to_milliseconds(match.group(1))
            end = to_milliseconds(match.group(3))
        except ValueError as error:
            issues.append(f"line {number}: {error}")
            continue
        if start >= end:
            issues.append(f"line {number}: cue start must be before cue end")
        if start < previous_start:
            issues.append(f"line {number}: cue starts are not in chronological order")
        previous_start = start
        cues += 1
    if cues == 0:
        issues.append("no subtitle timing lines found")
    return issues


def shift_srt(text, offset_ms):
    issues = validate_srt(text)
    if issues:
        raise ValueError("; ".join(issues))
    shifted = []
    for line in text.splitlines(keepends=True):
        ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        content = line.rstrip("\r\n")
        match = TIMING_LINE.fullmatch(content)
        if match:
            start = to_milliseconds(match.group(1)) + offset_ms
            end = to_milliseconds(match.group(3)) + offset_ms
            if max(0, start) >= max(0, end):
                raise ValueError("Offset collapses a cue to zero duration")
            content = from_milliseconds(start) + match.group(2) + from_milliseconds(end) + match.group(4)
        shifted.append(content + ending)
    return "".join(shifted)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate and shift SubRip subtitle timing.")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Validate an SRT file")
    check.add_argument("input", type=Path)
    shift = commands.add_parser("shift", help="Write a time-shifted SRT copy")
    shift.add_argument("input", type=Path)
    shift.add_argument("--offset-ms", type=int, required=True)
    shift.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        text = args.input.read_text(encoding="utf-8-sig")
        if args.command == "check":
            issues = validate_srt(text)
            if issues:
                print("\n".join(issues), file=sys.stderr)
                return 1
            print("SRT timing looks valid.")
            return 0
        output = Path(args.output)
        if output.exists():
            raise FileExistsError(f"Output already exists: {output}")
        result = shift_srt(text, args.offset_ms)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
        print(f"Wrote shifted subtitles to {output}")
        return 0
    except (OSError, ValueError) as error:
        print(f"subtitle-shift: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
