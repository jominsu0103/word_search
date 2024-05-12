<script>
  import Router from "svelte-spa-router";
  import Main from "./pages/Main.svelte";
  import Maker from "./pages/Maker.svelte";
  import "./css/style.css";
  import Mypage from "./pages/Mypage.svelte";
  import Login from "./pages/Login.svelte";
  import Signup from "./pages/Signup.svelte";
  import Game from "./pages/Game.svelte";
  const routes = {
    "/": Main,
    "/maker": Maker,
    "/mypage": Mypage,
    "/login": Login,
    "/signup": Signup,
    "/game/:gameId": Game,
  };
</script>

<Router {routes} />

<style></style>
