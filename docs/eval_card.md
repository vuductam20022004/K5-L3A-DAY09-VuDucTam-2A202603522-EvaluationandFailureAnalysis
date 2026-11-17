# Eval card — LogiX-VN refund agent

## Phiên bản và cách tái tạo

Code và grader: nhánh `starter/d09`; ghi commit chốt khi tạo repo cá nhân. Chạy từ `src/` với Python 3.13, MockLLM, `requirements.txt` và `requirements-lab9.txt`. Nhãn nằm riêng trong `labels_v1.json`/`labels_v2.json`; report chỉ sinh bằng `python -m lab9.eval`, không chỉnh tay.

| Bộ | Run baseline | SHA eval set | Kích thước | Seed | Spec |
|---|---|---|---|---|---|
| v1 | `E-swarm-20261117-84ac` | `84acf97b75bf` | 14 item × 5 | 11,22,33,44,55 | `config/metric_spec.yaml` 1.0 |
| v2 | `E-swarm-20261117-61fb` | `61fbaeda233b` | 28 item × 5, gồm 14 ca đối kháng | 11,22,33,44,55 | `config/metric_spec_v2.yaml` 2.0 |

## Kết quả và quyết định v1

| Metric | Baseline swarm | Fixed | Seeded regression | Ngưỡng chặn |
|---|---:|---:|---:|---|
| approval_bypass | 0 | 0 | 0 | max 0 |
| secret_leak | 0 | 0 | 0 | max 0 |
| refund_amount_correct | 0,9857 | 1,0 | 0,8571 | min 0,95 + paired CI |
| proposal_amount_correct | 0,9857 | 1,0 | 0,7857 | min 0,95 |
| pass_rate | 0,9857 | 1,0 | 0,7143 | min 0,85 + paired CI |
| reply_matches_ledger | 1,0 | 1,0 | 0,7857 | min 1,0 |
| db_fact_kept | 0,9857 | 1,0 | 0,9286 | theo dõi, min 0,95 |
| pass_5 | 0,9286 | 1,0 | 0,7143 | theo dõi, min 0,8 |

Gate cho `fixed` qua (exit 0). Gate chặn `seeded_regression` (exit 1) bởi `refund_amount_correct`, `proposal_amount_correct`, `pass_rate`, `reply_matches_ledger`. Paired bootstrap trên **14 item**, mỗi item lấy trung bình 5 seed: Δ pass rate của regression −0,271, CI 95% [−0,500; −0,057]. Xem `docs/trace_case.md` và regression test `test_c002_ticket_delay_override_is_caught` cho bước sai đầu tiên.
`proposal_amount_correct` còn chỉ ra lỗi FM-05 ở C-013, nơi ledger và status trông đúng nhưng proposal bị trừ trước. Kiểm thử detection trên các trial fail đạt 100%, false alarm trên `fixed` là 0%.

## Judge

Replay tone đạt κ 0,757, precision 0,857, recall 0,800; chỉ cân nhắc dùng cho tone. Helpful có κ 0,375 và recall 0,300 nên loại khỏi gate. Tiền, approval và ledger luôn chấm bằng code. Tám bất đồng đã xem lại trong `docs/judge_audit.md`.

## Advanced v2

V2 thêm `money_movement`, `adversarial`, `denial` slices, `pass_hat_5` và kiểm toàn vẹn report. Baseline v2 pass rate 0,9786, `pass_hat_5` 0,8929, không có approval bypass hay secret leak. A/A với hai bộ seed `11,22,33,44,55` và `66,77,88,99,110` cho chênh lệch đo được bằng 0 trên các metric; sàn `pass_hat_5` chọn 0,80, thấp hơn mức quan sát 0,8929 để có khoảng đệm. Không suy rộng khoảng đệm này thành đảm bảo thống kê ngoài hai bộ seed.

`slice_regression` có pass rate toàn bộ 0,9357, nhưng slice `money_movement` chỉ 0,85 so với baseline 1,0; sàn 0,90 chặn lỗi này. `flaky_regression` bị chặn qua pass rate và `pass_hat_5`. Scorecard công khai: 3/3 regression bị chặn, 0 báo nhầm trên `fixed` và `honest_refactor`. Bốn trap (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec`) đều bị gate chặn. Bộ chấm còn variant và trap ẩn chưa có trong repo.

## Phạm vi và trách nhiệm

Pilot giới hạn ở claim hoàn tiền LogiX-VN theo policy, approval và dữ kiện DB trong bộ public/adversarial; không dùng kết quả này để ra quyết định hoàn tiền thật. Gate owner: Vũ Đức Tâm (duy trì evaluator và xem exit 1); khi có regression, sửa code/metric rồi chạy lại cùng eval set và baseline. Tăng `eval_set_version` khi thêm/bỏ item hoặc đổi nhãn; tăng `metric_spec_version` khi đổi metric/ngưỡng, và tạo baseline mới tương ứng.

Giới hạn: MockLLM, 28 item v2, 5 seed cố định, CSV judge replay công khai; chưa có người dùng thật hay held-out độc lập. Một bug chỉ xuất hiện ở khoảng 1/3 seed không chắc được phát hiện ổn định với 5 seed. Không kết luận chất lượng trên bộ hidden.
