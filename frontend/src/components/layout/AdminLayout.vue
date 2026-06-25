<template>
  <div style="display:flex;height:100vh;">
    <div style="width:200px;background:#001529;color:#fff;padding:20px;">
      <h3 style="color:#fff;">后台管理</h3>
      <div style="margin-top:20px;">
        <div style="padding:10px;cursor:pointer;" @click="$router.push('/admin')">📊 仪表盘</div>
        <div style="padding:10px;cursor:pointer;" @click="$router.push('/admin/reports')">📋 举报管理</div>
        <div style="padding:10px;cursor:pointer;" @click="$router.push('/admin/users')">👤 用户管理</div>
        <div style="padding:10px;cursor:pointer;" @click="$router.push('/admin/words')">🔒 敏感词管理</div>
      </div>
    </div>
    <div style="flex:1;padding:20px;background:#f0f2f5;overflow:auto;">
      <router-view />
    </div>
  </div>
</template>