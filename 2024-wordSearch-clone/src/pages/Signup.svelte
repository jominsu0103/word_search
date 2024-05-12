<script>
  import Nav from "../components/Nav.svelte";
  let email = "";
  let password = "";
  let nickname = "";

  const BASE_URL = "http://localhost:8000";

  export async function handleSignup() {
    console.log(`Email: ${email} Password: ${password} nickname: ${nickname}`);
    try {
      const userData = {
        email: email,
        password: password,
        nickname: nickname,
      };
      const response = await fetch(`${BASE_URL}/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      console.log("message:", data);

      if (response.status === 201) {
        window.location.hash = "/"
      }
    } catch (error) {
      console.error("회원 가입 실패:", error.message);
    }
  }
  function handleSignupKeyDown(event) {
    if (event.key === "Enter") {
      handleSignup();
    }
  }
</script>

<Nav location="signup"></Nav>

<main>
  <div class="signup-container">
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
        placeholder="비밀번호를 작성해주세요"
      />
    </div>
    <div class="nickname-container">
      <label for="nickname">Nickname</label>
      <br />
      <input
        on:keydown={handleSignupKeyDown}
        id="nickname"
        bind:value={nickname}
        type="text"
        placeholder="닉네임을 작성해주세요"
      />
    </div>
    <div
      class="signup-btn"
      role="button"
      tabindex="0"
      on:click={handleSignup}
      on:keydown={handleSignupKeyDown}
    >
      Sign Up
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .signup-container {
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

  .signup-btn {
    width: 250px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: #aaeb9f;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s; /* hover 효과 추가 */
  }

  .signup-btn:hover {
    background-color: #85bd8b; /* hover 효과 색상 변경 */
  }

  .email-container input,
  .password-container input,
  .nickname-container input {
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
</style>
