from __future__ import annotations
import argparse
from workflow_utils import confirm_gate
def main():
    ap=argparse.ArgumentParser(description="人工确认当前闸门后解锁下一阶段")
    ap.add_argument("gate")
    a=ap.parse_args(); confirm_gate(a.gate); print(f"[OK] 已确认 {a.gate}")
if __name__ == "__main__": main()
