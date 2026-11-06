/* Weighted greedy modularity, matching wording_communities.py. */
function fitWordingGroups(nodes,edges,resolution=1){
 const ids=nodes.map(n=>typeof n==='object'?n.id:n).sort((a,b)=>a-b),members=new Map(ids.map(id=>[id,[id]])),degree=new Map(ids.map(id=>[id,0])),cross=new Map();
 const key=(a,b)=>Math.min(a,b)+'|'+Math.max(a,b);let total=0;
 for(const e of edges){if(!members.has(e.source)||!members.has(e.target))continue;degree.set(e.source,degree.get(e.source)+e.weight);degree.set(e.target,degree.get(e.target)+e.weight);cross.set(key(e.source,e.target),e.weight);total+=e.weight;}
 if(!total)return Object.fromEntries(ids.map(id=>[id,-1]));
 while(true){const keys=[...members.keys()].sort((a,b)=>a-b);let best=null,gain=1e-12;
  for(let at=0;at<keys.length;at++)for(let next=at+1;next<keys.length;next++){const i=keys[at],j=keys[next],delta=(cross.get(key(i,j))||0)/total-resolution*degree.get(i)*degree.get(j)/(2*total*total);if(delta>gain){gain=delta;best=[i,j];}}
  if(!best)break;const [i,j]=best;members.set(i,members.get(i).concat(members.get(j)));members.delete(j);degree.set(i,degree.get(i)+degree.get(j));degree.delete(j);
  for(const k of members.keys())if(k!==i){const a=key(i,k),b=key(j,k);cross.set(a,(cross.get(a)||0)+(cross.get(b)||0));cross.delete(b);}cross.delete(key(i,j));
 }
 const linked=new Set(edges.flatMap(e=>[e.source,e.target])),groups=[...members.values()].filter(g=>g.some(id=>linked.has(id))).map(g=>g.sort((a,b)=>a-b)).sort((a,b)=>b.length-a.length||a[0]-b[0]);
 const result=Object.fromEntries(ids.map(id=>[id,-1]));groups.forEach((g,index)=>g.forEach(id=>result[id]=index));return result;
}
