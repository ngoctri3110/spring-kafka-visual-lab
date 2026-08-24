# Kafka Spring Boot Visual Lab

[![Validate course](https://github.com/ngoctri3110/spring-kafka-visual-lab/actions/workflows/validate-course.yml/badge.svg)](https://github.com/ngoctri3110/spring-kafka-visual-lab/actions/workflows/validate-course.yml)
[![GitHub Pages](https://img.shields.io/badge/Learn%20online-GitHub%20Pages-1facc0)](https://ngoctri3110.github.io/spring-kafka-visual-lab/)

Khóa học tĩnh bằng HTML giúp học Apache Kafka với Java/Spring Boot qua sơ đồ, mô phỏng tương tác, bài thực hành và checklist ghi nhớ. Lộ trình gồm 12 trang bài học, từ nền tảng đến capstone Order Platform.

## Mở khóa học

Học trực tuyến: **https://ngoctri3110.github.io/spring-kafka-visual-lab/**

Trang bắt đầu: [`docs/index.html`](docs/index.html)

Để các tính năng trình duyệt hoạt động giống GitHub Pages, nên chạy một web server cục bộ tại thư mục gốc:

```bash
python -m http.server 8765
```

Sau đó mở `http://127.0.0.1:8765/docs/`.

Tiến độ học được lưu bằng `localStorage`. Không cần tài khoản, nhưng dữ liệu không tự đồng bộ giữa các trình duyệt hoặc thiết bị.

## Đưa lên GitHub Pages

1. Đẩy repository lên GitHub.
2. Mở **Settings → Pages**.
3. Trong **Build and deployment**, chọn **Deploy from a branch**.
4. Chọn branch `main`, thư mục `/docs`, rồi **Save**.

File `docs/.nojekyll` giữ nguyên các tài nguyên tĩnh, còn workflow `.github/workflows/validate-course.yml` tự kiểm tra liên kết nội bộ và cấu trúc khóa học mỗi lần push hoặc mở pull request.

## Kiểm tra trước khi public

```bash
python scripts/validate_course.py
```

Tài liệu tham khảo trong khóa học chỉ trỏ đến nguồn công khai, chính thức của Apache Kafka, Spring, Debezium, Testcontainers và PostgreSQL.

Repository hiện chưa khai báo giấy phép sử dụng. Hãy thêm `LICENSE` phù hợp trước khi cho phép người khác sao chép hoặc chỉnh sửa nội dung.

## Chủ đề

`apache-kafka` · `spring-kafka` · `spring-boot` · `java` · `visual-learning` · `distributed-systems` · `event-driven-architecture` · `transactional-outbox`
