<script>
  import Nav from "../components/Nav.svelte";
  let email = "";
  let password = "";

  const BASE_URL = "http://localhost:8000";

  const handleGoogleLogin = async () => {
    try {
      const response = await fetch(`${BASE_URL}/google/login`);
      const data = await response.json();

      // JSON 응답에서 URL 값 추출
      const redirectUrl = data.authorization_url;
      console.log("Received redirect URL:", redirectUrl);
      console.log(data)

      // // Redirect to the Google login page
      window.location.href = data.url
    } catch (error) {
      console.error("Google login error:", error.message);
    }
  };

  export async function handleSignin() {
    console.log(`Email: ${email} Password: ${password}`);
    try {
      const userData = {
        email: email,
        password: password,
      };
      const response = await fetch(`${BASE_URL}/signin`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      if (response.status === 200) {
        localStorage.setItem("accessToken", data.access_token);
        console.log("로그인 성공!!");
        window.location.hash = "/";
      }
    } catch (error) {
      console.log("로그인 실패:", error.message);
    }
  }
  function handleSignupKeyDown(event) {
    if (event.key === "Enter") {
      handleSignin();
    }
  }
</script>

<Nav location="login"></Nav>

<main>
  <div class="login-container">
    <div class="email-container">
      <label for="email">Email</label>
      <br />
      <input
        id="email"
        bind:value={email}
        type="email"
        placeholder="이메일을 작성해주세요"
      />
    </div>
    <div class="password-container">
      <label for="password">Password</label>
      <br />
      <input
        id="password"
        bind:value={password}
        type="password"
        on:keydown={handleSignupKeyDown}
        placeholder="비밀번호를 작성해주세요"
      />
    </div>
    <div
      role="button"
      tabindex="0"
      class="signin-btn"
      on:click={handleSignin}
      on:keydown={handleSignupKeyDown}
    >
      Sign In
    </div>
    <div class="other">------ Or continue with ------</div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div on:click={handleGoogleLogin} class="google-container">
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

  ::placeholder {
    font-size: 10px;
  }
  .google-container {
    cursor: pointer;
  }
</style>
