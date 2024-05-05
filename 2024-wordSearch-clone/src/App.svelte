<script>
  import Router from "svelte-spa-router";
  import Main from "./pages/Main.svelte";
  import Maker from "./pages/Maker.svelte";
  import "./css/style.css";
  import Mypage from "./pages/Mypage.svelte";
  const routes = {
    "/": Main,
    "/maker": Maker,
    "/mypage": Mypage,
  };
</script>

<Router {routes} />

<style></style>
