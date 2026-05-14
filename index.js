export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    const corsHeaders = {
      "Access-Control-Allow-Origin": "https://my-workshopapppp.pages.dev",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    if (request.method === "POST" && url.pathname === "/ai-generate") {
      try {
        const { prompt } = await request.json();
        
        // Gemini 3.1 Pro + Strict JSON Config
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-latest:generateContent?key=${env.GEMINI_API_KEY}`;

        const aiResponse = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ role: "user", parts: [{ text: prompt }] }],
            // یہ حصہ لازمی ہے:
            generationConfig: {
              responseMimeType: "application/json",
              temperature: 0.7
            }
          })
        });

        const data = await aiResponse.json();
        return new Response(JSON.stringify(data), { 
          headers: { ...corsHeaders, "Content-Type": "application/json" } 
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
      }
    }

    return new Response("Mistri Backend Online", { headers: corsHeaders });
  }
};
