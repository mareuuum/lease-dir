(function(){
  try{
    var key='ab_ver';
    var v = localStorage.getItem(key);
    if(!v){ v = Math.random()<0.5 ? 'A' : 'B'; localStorage.setItem(key, v); }
    // 例: 会議室LPのA/B切替（存在しない場合は無視）
    if(location.pathname === '/lp/meeting-rooms.html'){
      if(v==='A'){ location.replace('/lp/meeting-rooms-a.html'); }
      else { location.replace('/lp/meeting-rooms-b.html'); }
    }
  }catch(e){}
})();
