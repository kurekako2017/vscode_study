document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('btn');
  var msg = document.getElementById('msg');
  if (btn) {
    btn.addEventListener('click', function () {
      msg.textContent = '按钮已点击 — 欢迎使用 VS Code 开发静态站点！';
    });
  }
});
