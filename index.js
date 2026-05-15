export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    if (request.method === "POST" && url.pathname === "/ai-generate") {
      try {
        const { prompt } = await request.json();
        
        // 100% Gemini 3.1 Pro Latest
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-latest:generateContent?key=${env.GEMINI_API_KEY}`;

        const aiResponse = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ role: "user", parts: [{ text: prompt }] }],
            // یہ ہے وہ ماسٹر سٹریٹیجی جو اے آئی کو فالتو بات نہیں کرنے دے گی
            generationConfig: {
              responseMimeType: "application/json",
              responseSchema: {
                type: "OBJECT",
                properties: {
                  updatedFiles: {
                    type: "ARRAY",
                    items: {
                      type: "OBJECT",
                      properties: {
                        name: { type: "STRING" },
                        content: { type: "STRING" },
                        language: { type: "STRING" },
                        path: { type: "STRING" }
                      },
                      required: ["name", "content", "language"]
                    }
                  },
                  summary: { type: "STRING" }
                },
                required: ["updatedFiles", "summary"]
              }
            }
          })
        });

        if (!aiResponse.ok) {
          const errData = await aiResponse.json();
          throw new Error(errData.error?.message || "Google API Error");
        }

        const data = await aiResponse.json();
        return new Response(JSON.stringify(data), { 
          headers: { ...corsHeaders, "Content-Type": "application/json" } 
        });

      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
      }
    }
    
    return new Response("Mistri Backend 3.1 Pro (Strict Mode) Online", { headers: corsHeaders });
  }
};
        
