const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target:
        process.env.REACT_APP_CTX === "docker"
          ? "http://server:3001"
          : "http://localhost:3001",
      changeOrigin: true,
    })
  );
};
