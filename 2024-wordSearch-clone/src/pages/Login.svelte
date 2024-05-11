<script>
  import Nav from "../components/Nav.svelte";
</script>

<Nav location="login"></Nav>

<main>
  <div class="login-container">
    <div class="email-container">
      <label for="email">Email</label>
      <br />
      <input id="email" type="email" placeholder="이메일을 작성해주세요"/>
    </div>
    <div class="password-container">
      <label for="password">Password</label>
      <br />
      <input id="password" type="password" placeholder="비밀번호를 작성해주세요"/>
    </div>
    <div class="signin-btn">Sign In</div>
    <div class="other">------ Or continue with ------</div>
    <div class="google-container">
      <img src="/assets/google.svg" alt="" />
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin-top: 200px;
    gap: 25px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
    width: 300px; /* 너비 수정 */
    padding: 20px; /* 내부 여백 추가 */
    border-radius: 10px; /* 테두리 모서리 둥글게 처리 */
  }

  .signin-btn {
    width: 250px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: #d0aaf1;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s; /* hover 효과 추가 */
  }

  .signin-btn:hover {
    background-color: #b37eed; /* hover 효과 색상 변경 */
  }

  .email-container input,
  .password-container input {
    margin-top: 10px;
    width: 250px;
    height: 30px;
    border-radius: 10px;
    border: 1px solid #c1c1c2;
    padding: 5px; /* 내부 여백 추가 */
  }

  ::placeholder{
    font-size: 10px;
  }
</style>
