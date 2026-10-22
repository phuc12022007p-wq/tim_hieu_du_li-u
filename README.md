# Góc Nhìn Dữ Liệu — ABC-27

Tác giả: Huỳnh Thanh Phúc.
Website tĩnh HTML, CSS, JavaScript. Không cần cài thư viện hoặc build.

## Đưa lên GitHub Pages

1. Giải nén goc-nhin-du-lieu-github.zip.
2. Đăng nhập GitHub, nhấn dấu + > New repository.
3. Đặt tên goc-nhin-du-lieu, chọn Public, nhấn Create repository.
4. Chọn uploading an existing file (hoặc Add file > Upload files).
5. Kéo tất cả nội dung bên trong thư mục đã giải nén lên: index.html, style.css, script.js, assets, README.md và .nojekyll. Không tải cả tệp ZIP. index.html phải nằm ngay ở thư mục gốc repository.
6. Nhấn Commit changes.
7. Mở Settings > Pages. Trong Build and deployment, chọn Deploy from a branch.
8. Chọn nhánh main và thư mục / (root), rồi Save.
9. Đợi triển khai hoàn tất, mở đường dẫn GitHub Pages hiện trong Settings > Pages.

## Cấu trúc

- index.html: toàn bộ bố cục và nội dung.
- style.css: giao diện và bố cục điện thoại.
- script.js: các tương tác, đọc CSV và mô phỏng nến.
- assets/: 12 hình từ báo cáo, PDF đầy đủ và main4.py.
- .nojekyll: phục vụ nguyên trạng các tệp tĩnh.

## Xem thử

Mở index.html bằng trình duyệt, hoặc dùng Live Server trong VS Code.

## Dữ liệu tương tác

Các hình và bảng trong báo cáo xem được ngay. Chọn tab Tương tác & phát lại, nạp abc-27.csv gồm 365 dòng × 7 cột số dương, không có tiêu đề. Khi đó có thể xem nến Nhật 5 ngày, đường Close và dải High–Low, rê chuột/chạm để xem số liệu, chọn nến bằng thanh trượt và phát lại 120 giây. CSV được xử lý trên trình duyệt, không tải lên máy chủ.

Tệp CSV và video MP4 chưa có trong gói này. Mã Python cần abc-27.csv, pandas, numpy, matplotlib và FFmpeg để xuất stock_simulation_2min.mp4. Biểu đồ trên web được viết bằng JavaScript; Python không chạy trực tiếp trên GitHub Pages.

## Cập nhật

Sửa tệp, tải bản mới lên repository và Commit changes. GitHub Pages triển khai lại sau mỗi lần cập nhật nhánh đã chọn.

Dữ liệu phục vụ học tập. Quy ước lịch: một năm không nhuận; không phải lịch giao dịch thực tế.
