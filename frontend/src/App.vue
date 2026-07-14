<template>
  <div class="mygumi-app">
    <nav style="padding: 20px; background: #D0E7FF; font-weight: bold;">
      <span style="margin-right: 20px; color: #0369A1;">☁️ 마이구미</span>
      <router-link to="/" style="margin-right: 15px;">지도 탐색</router-link>
      <router-link to="/board" style="margin-right: 15px;">익명 게시판</router-link>
      <router-link to="/course">마이 코스</router-link>
    </nav>

    <main style="padding: 20px;">
      <router-view></router-view>
    </main>
  </div>
</template>