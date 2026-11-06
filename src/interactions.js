/* Pinned vis-network 9.1.9: preserve settled geometry while retaining elastic
   interactions. This affects screen positions only, never network weights. */
function installElasticLayout(graph){
  const physics=graph.physics;
  const originalMove=physics.moveNodes;
  const state={ready:false,home:{},baseline:{}};
  graph.elasticLayout=state;
  function capture(){
    if(state.ready)return;
    // Native forces at the chosen resting layout are balanced out below. This
    // makes that layout an equilibrium instead of continually re-optimizing it.
    physics.gravitySolver.solve();physics.nodesSolver.solve();physics.edgesSolver.solve();
    for(const id of physics.physicsBody.physicsNodeIndices){
      const node=graph.body.nodes[id],force=physics.physicsBody.forces[id];
      state.home[id]={x:node.x,y:node.y};
      state.baseline[id]={x:force.x,y:force.y};
      const velocity=physics.physicsBody.velocities[id];
      if(velocity){velocity.x=0;velocity.y=0;}
    }
    state.ready=true;
  }
  physics.moveNodes=function(){
    if(state.ready){
      for(const id of this.physicsBody.physicsNodeIndices){
        const node=graph.body.nodes[id],home=state.home[id],base=state.baseline[id];
        const force=this.physicsBody.forces[id];
        if(!home||!base||!force)continue;
        const stiffness=.045*node.options.mass;
        force.x-=base.x+stiffness*(node.x-home.x);
        force.y-=base.y+stiffness*(node.y-home.y);
      }
    }
    return originalMove.apply(this,arguments);
  };
  graph.once('stabilizationIterationsDone',capture);
  // A settled or empty small graph can finish before the iteration limit.
  graph.once('stabilized',capture);
}

/* Emphasize direct displayed neighbors; preserve severity hues and graph data. */
function installNeighborhoodFocus(graph){
  const nodeData=graph.body.data.nodes,edgeData=graph.body.data.edges;
  const baseNodes=nodeData.get().map(n=>({id:n.id,opacity:n.opacity??1,font:{...n.font}}));
  const baseEdges=edgeData.get().map(e=>({id:e.id,from:e.from,to:e.to,color:{...e.color}}));
  let hovered=null,locked=null,applied=undefined;
  function paint(){
    const focus=hovered??locked;if(focus===applied)return;applied=focus;
    const neighbors=new Set(focus===null?[]:[focus]);
    if(focus!==null)for(const e of baseEdges){if(e.from===focus)neighbors.add(e.to);if(e.to===focus)neighbors.add(e.from);}
    nodeData.update(baseNodes.map(n=>{
      const bright=focus===null||neighbors.has(n.id);
      return {id:n.id,opacity:bright?n.opacity:.13,font:{...n.font,color:bright?n.font.color:'rgba(35,62,82,0.18)',strokeColor:bright?n.font.strokeColor:'rgba(255,255,255,0.15)'}};
    }));
    edgeData.update(baseEdges.map(e=>{
      const incident=e.from===focus||e.to===focus;
      return {id:e.id,color:focus===null?{...e.color}:incident?{...e.color,color:'#007e80',opacity:.85}:{...e.color,opacity:.055}};
    }));
  }
  graph.neighborhoodFocus={select(id){locked=id;paint();},clear(){hovered=null;locked=null;paint();},get current(){return hovered??locked;}};
  graph.on('hoverNode',event=>{hovered=event.node;paint();});
  graph.on('blurNode',()=>{hovered=null;paint();});
  graph.on('dragStart',()=>{hovered=null;paint();});
}
