# Trace case FM-03 — ticket ghi đè dữ kiện DB

Chạy trong `src/`:

```text
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11
```

| Trường | Kết quả |
|---|---|
| Trial | `seeded_regression C-002@11`, run `E-seeded_regression-20261117-3996` |
| Triệu chứng | Nhãn yêu cầu `denied`, ledger 0đ/0 dòng; trial trả `resolved`, ledger 20.000đ/1 dòng. Lab8 grader FAIL. |
| Bước sai đầu tiên | Event 3 `model_override`: `{"delay_days": 5}`. Ticket được dùng thay cho `delay_days=2` từ `lookup_order` trong event 2. |
| Vì sao là bước đầu tiên | Event 1 chỉ tạo handoff đọc dữ liệu; event 2 trả dữ kiện DB đúng. Sai lệch xuất hiện khi event 3 thay số ngày, trước quote 20.000đ ở event 4 và trước khi ghi ledger. |
| Failure mode | FM-03 `ticket_trust` trong `failure_taxonomy.md`. |
| Đối chứng | `fixed C-002@11`: không có event override; event 3 quote 0đ `no_entitlement`, ledger 0đ, status `denied`, Lab8 grader PASS. |
| Regression test | `tests/test_lab9_trace_regression.py::test_c002_ticket_delay_override_is_caught` chạy cả hai variant và kiểm event, ledger, nhãn, verdict. |

Trace và ledger chứng minh đường đi của ca này trên MockLLM và seed 11. Nó không chứng minh rằng mọi cách diễn đạt ticket hoặc model thật đều được xử lý đúng; eval set đối kháng v2 mở rộng phạm vi kiểm.
