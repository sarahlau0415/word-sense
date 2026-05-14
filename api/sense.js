const { generateSense } = require("../lib/generate-sense");

function sendJson(response, statusCode, payload) {
  response.statusCode = statusCode;
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.end(JSON.stringify(payload));
}

function readBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.on("data", chunk => {
      body += chunk;
      if (body.length > 20000) {
        request.destroy();
        reject(new Error("Request body is too large."));
      }
    });
    request.on("end", () => resolve(body));
    request.on("error", reject);
  });
}

module.exports = async function handler(request, response) {
  if (request.method !== "POST") {
    response.setHeader("Allow", "POST");
    return sendJson(response, 405, { error: "Method not allowed" });
  }

  let payload;
  try {
    payload = JSON.parse(await readBody(request));
  } catch (error) {
    return sendJson(response, 400, { error: "Invalid JSON request body." });
  }

  try {
    const result = await generateSense(payload);
    return sendJson(response, 200, result);
  } catch (error) {
    return sendJson(response, error.statusCode || 500, {
      error: error.message || "Could not generate a Word Sense answer."
    });
  }
};
