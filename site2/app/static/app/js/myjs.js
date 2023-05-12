function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//Đăng xuất
function logout() {
    $.ajax({
      url: '/dangxuat/',
      type: 'POST',
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
      data: {},
      success: function(response) {
        if (response.status === 'ok') {
          // Xử lý khi đăng xuất thành công, ví dụ chuyển hướng trang
          window.location.href = '';
        } else {
          // Xử lý khi đăng xuất thất bại, ví dụ hiển thị thông báo lỗi
          alert('Có lỗi xảy ra khi đăng xuất!');
        }
      },
      error: function(xhr, status, error) {
        // Xử lý khi có lỗi xảy ra trong quá trình gửi yêu cầu đăng xuất
        alert('Có lỗi xảy ra khi gửi yêu cầu đăng xuất!');
      }
    });
  }
  $(document).ready(function() {
    $('#confirmLogout').click(logout);
  });
 //Tạo sự kiện bấm nút xóa ở loại món trả về id loại
  const nutXoaloai = document.querySelectorAll('.xoaloainame');
  const loaiidIp = document.querySelector('#loai-id');
  nutXoaloai.forEach(button => {
    button.addEventListener('click', (event) => {
      const productId = event.target.getAttribute('data-id');
      loaiidIp.value = productId;
    });
  });
//Tạo sự kiện bấm nút xóa ở món ăn trả về id món
  const nutXoamon = document.querySelectorAll('.xoamonname');
  const monidIp = document.querySelector('#mon-id');  
  nutXoamon.forEach(button => {
    button.addEventListener('click', (event) => {
      const productId = event.target.getAttribute('data-id');
      monidIp.value = productId;
    });
  });
//Tạo sự kiện bấm nút xóa ở kho hàng trả về id loại nvl
  const nutXoakho = document.querySelectorAll('.xoakhoname');
  const khoidIp = document.querySelector('#kho-id');
  nutXoakho.forEach(button => {
    button.addEventListener('click', (event) => {
      const productId = event.target.getAttribute('data-id');
      khoidIp.value = productId;
    });
  });
//Tạo sự kiện bấm nút sửa ở kho hàng trả về id loại nvl
  const nutSuakho = document.querySelectorAll('.suakhoname');
  const khosuaidIp = document.querySelector('#suakho');
  nutSuakho.forEach(button => {
    button.addEventListener('click', (event) => {
      const productId = event.target.getAttribute('data-sua-id');
      khosuaidIp.value = productId;
      console.log(productId);
    });
  });
var radios = document.getElementsByName("trangthaithem");

for (var i = 0; i < radios.length; i++) {
  radios[i].addEventListener("change", function(event) {
    var selected = event.target.value;
    if (selected == "themsoluong") {
      mathem.removeAttribute("disabled");
      tenthem.setAttribute("disabled", "disabled");
      motathem.setAttribute("disabled", "disabled");
      dvtthem.setAttribute("disabled", "disabled");
      soluongthem.setAttribute("disabled", "disabled");
      giatienthem.setAttribute("disabled", "disabled");
      slmoi.removeAttribute("disabled");

    } else {
      mathem.setAttribute("disabled", "disabled");
      slmoi.setAttribute("disabled", "disabled");
      tenthem.removeAttribute("disabled");
      motathem.removeAttribute("disabled");
      soluongthem.removeAttribute("disabled");
      dvtthem.removeAttribute("disabled");
      giatienthem.removeAttribute("disabled");
    }
  });
}

const nutXoanhanvien = document.querySelectorAll('.xoanvname');
const nhanvienxoaidIp = document.querySelector('#nhanvien-id');
  
  nutXoanhanvien.forEach(button => {
    button.addEventListener('click', (event) => {
      const productId = event.target.getAttribute('data-nhanvien-id');
    
      nhanvienxoaidIp.value = productId;
    });
  });

//Xử lý để gọi món
  const nutGoimon = document.querySelectorAll('.goimon');
    nutGoimon.forEach(button => {
      button.addEventListener('click', (event) => {
        const productId = event.target.getAttribute('data-goimon-id');
        $.ajax({
          url: '',
          method: 'POST',
          data: {goimonid: productId},
          beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
          success: function(response) {
              // Xử lý phản hồi từ view
              location.reload();
              alert("Đã thêm");
          },
          error: function() {
              // Xử lý lỗi
          }
      });
      });
    });
   
//Tùy chọn loại để hiện phương thức thanh toán
    var loai = document.getElementsByName("loai");
    for (var i = 0; i < loai.length; i++) {
      loai[i].addEventListener("change", function(event) {
        var selected = event.target.value;
        var div = document.getElementById("phuongthuc");
        if (selected == "grab") {
          div.style.display = "none";
        }
        else{
          div.style.display = "block";
        }
      });
    }

//Xóa đơn hàng
    const nutXoadon = document.querySelectorAll('.xoadonhangname');
    const donxoaidIp = document.querySelector('#don-id');
      nutXoadon.forEach(button => {
        button.addEventListener('click', (event) => {
          const productId = event.target.getAttribute('data-id');
          donxoaidIp.value = productId;
        });
      });

 