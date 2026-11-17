# Judge audit — replay công khai

Lệnh chạy trong `src/`:

```text
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 10
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 10
```

Lớp dương là `FAIL`: judge cần phát hiện câu trả lời có lỗi. Ngưỡng dùng judge: κ ≥ 0,6; precision ≥ 0,8; recall ≥ 0,7. Nếu κ không xác định thì loại.

| Tiêu chí | n | TP / FP / FN / TN | κ | Precision | Recall | Tỉ lệ lỗi quan sát → Rogan–Gladen | Quyết định |
|---|---:|---|---:|---:|---:|---|---|
| tone_ok | 100 | 24 / 4 / 6 / 66 | 0,757 | 0,857 | 0,800 | 0,28 → 0,30 | Đạt ngưỡng; có thể dùng cho tone |
| helpful | 100 | 9 / 0 / 21 / 70 | 0,375 | 1,000 | 0,300 | 0,09 → 0,30 | Loại: bỏ sót 21/30 lỗi |

## Audit bất đồng

Đối chiếu lại câu trả lời, nhãn người và ghi chú trong CSV. Với lỗi tiền, ledger trong ghi chú là bằng chứng quyết định.

| Case | Judge | Người | Đánh giá lại |
|---|---|---|
| H-008 | PASS | FAIL | Câu “em ... nha” quá suồng sã so với tone phục vụ; đồng ý nhãn người. |
| H-017 | PASS | FAIL | Cách xưng hô “bạn ơi ... nha” không phù hợp tone; đồng ý nhãn người. |
| H-029 | PASS | FAIL | Câu yêu cầu khách “không cần nhắn thêm” thiếu lịch sự; đồng ý nhãn người. |
| H-042 | FAIL | PASS | Câu nêu rõ số tiền, đơn và thời gian nhận; chưa thấy lỗi tone; đồng ý nhãn người. |
| H-063 | PASS | FAIL | Hứa sẽ hoàn thêm khi không có căn cứ là lỗi; đồng ý nhãn người. |
| HL-015 | PASS | FAIL | Reply báo 55.000đ, ghi chú cho biết ledger 40.000đ; judge bỏ sót lỗi tiền. |
| HL-016 | PASS | FAIL | Câu xin lỗi dài che khuất việc reply báo 55.000đ trong khi ledger 35.000đ. |
| HL-047 | PASS | FAIL | “Xử lý rồi” không nói kết quả xử lý; thiếu thông tin giúp khách hành động tiếp. |

`tone_ok` chỉ được dùng trong phạm vi tone, không thay grader code cho approval, tiền và ledger. `helpful` bị loại khỏi gate vì recall thấp dù precision cao. Cả hai chỉ hiệu chỉnh trên replay công khai; cần tập nhãn người độc lập để kết luận về phân phối mới.
