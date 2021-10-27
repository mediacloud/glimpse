// initialize vega-lite

// setup API options
const vlOptions = {
  config: {
    // Vega-Lite default configuration
  },
  init: (view) => {
    // initialize tooltip handler
    view.tooltip(new vegaTooltip.Handler().call);
  },
  view: {
    // view constructor options
    renderer: "canvas",
  },
};

// register vega and vega-lite with the API
vl.register(vega, vegaLite, vlOptions);
