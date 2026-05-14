export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    const corsHeaders = {
      "Access-Control-Allow-Origin": "https://my-workshopapppp.pages.dev",
      "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    try {
      // 1. AI Generation End-point (Gemini 3.1 Pro)
      if (request.method === "POST" && url.pathname === "/ai-generate") {
        const { prompt } = await request.json();
        
        // یہاں ہم نے لیٹسٹ ماڈل 3.1 پرو سیٹ کر دیا ہے
        const targetModel = "gemini-3.1-pro-latest";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:generateContent?key=${env.GEMINI_API_KEY}`;

        const aiResponse = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ role: "user", parts: [{ text: prompt }] }]
          })
        });

        const data = await aiResponse.json();
        return new Response(JSON.stringify(data), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
      }

      // 2. باقی تمام اینڈ پوائنٹس (List, Load, Save, Delete) ویسے ہی رہیں گے
      if (request.method === "GET" && url.pathname === "/list") {
        const { results } = await env.DB.prepare("SELECT project_name, repo_name, last_synced FROM ayesha_multi_projects ORDER BY last_synced DESC").all();
        return new Response(JSON.stringify(results), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
      }

      if (request.method === "GET" && url.pathname === "/load") {
        const name = url.searchParams.get("name");
        const result = await env.DB.prepare("SELECT * FROM ayesha_multi_projects WHERE project_name = ?").bind(name).first();
        return new Response(result ? JSON.stringify(result) : "{}", { headers: { ...corsHeaders, "Content-Type": "application/json" } });
      }

      if (request.method === "POST" && url.pathname === "/save") {
        const { project_name, repo_name, project_state_json } = await request.json();
        await env.DB.prepare(
          "INSERT OR REPLACE INTO ayesha_multi_projects (project_name, repo_name, project_state_json, last_synced) VALUES (?, ?, ?, CURRENT_TIMESTAMP)"
        ).bind(project_name, repo_name, project_state_json).run();
        return new Response(JSON.stringify({ success: true, message: "Project Saved" }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
      }

      if (request.method === "DELETE" && url.pathname === "/delete") {
        const name = url.searchParams.get("name");
        await env.DB.prepare("DELETE FROM ayesha_multi_projects WHERE project_name = ?").bind(name).run();
        return new Response(JSON.stringify({ success: true, message: "Project Deleted" }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
      }

    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } });
    }
    
    return new Response("Mistri AI Backend Live (3.1 Pro Enabled)", { headers: corsHeaders });
  }
};
