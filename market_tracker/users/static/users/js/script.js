! function(e) {
  function o(e, o) {
    l++, d = l / c, TweenLite.to(g, .7, {
      progress: d,
      ease: Linear.easeNone
    })
  }

  function t() {
    d = Math.round(100 * g.progress())
  }

  function a() {
    var o = new TimelineMax;
    return o.to(e(".progress"), .3, {
      y: 100,
      autoAlpha: 0,
      ease: Back.easeIn
    }).set(e("body"), {
      className: "-=is-loading"
    }).set(e("#intro"), {
      className: "+=is-loaded"
    }).to(e("#preloader"), .7, {
      yPercent: 100,
      ease: Power4.easeInOut
    }).set(e("#preloader"), {
      className: "+=is-hidden"
    })
  }
  var r = new ScrollMagic.Controller,

    l = 0,
    c = e(".bcg").length

  e(".bcg").imagesLoaded({
    background: !0
  }).progress(function(e, t) {
    o()
  });
  var g = new TimelineMax({
    paused: !0,
    onUpdate: t,
    onComplete: a
  });
  if (g.to(e(".progress span"), 1, {
      width: 100,
      ease: Linear.easeNone
    })) {


  }
}(jQuery);