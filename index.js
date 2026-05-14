export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin");
    
    // صرف آپ کی ورکشاپ کے لنک کو اجازت دینے کے لیے CORS Headers
    const corsHeaders = {
      "Access-Control-Allow-Origin": "https://my-app-workshop.onhercules.app",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    // Preflight request ہینڈل کرنا
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // ڈیٹا سیو کرنے کے لیے (POST /save)
      if (request.method === "POST" && url.pathname === "/save") {
        const { repo_name, project_state_json } = await request.json();
        
        await env.DB.prepare(
          "INSERT OR REPLACE INTO project_backups (repo_name, project_state_json, last_synced) VALUES (?, ?, CURRENT_TIMESTAMP)"
        ).bind(repo_name, project_state_json).run();
        
        return new Response(JSON.stringify({ success: true, message: "Project backed up to D1" }), { 
          headers: { ...corsHeaders, "Content-Type": "application/json" } 
        });
      }

      // ڈیٹا لوڈ کرنے کے لیے (GET /load?repo=name)
      if (request.method === "GET" && url.pathname === "/load") {
        const repo = url.searchParams.get("repo");
        if (!repo) return new Response("Missing repo param", { status: 400, headers: corsHeaders });

        const result = await env.DB.prepare(
          "SELECT project_state_json FROM project_backups WHERE repo_name = ?"
        ).bind(repo).first();
        
        return new Response(result ? result.project_state_json : JSON.stringify({}), {
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { 
        status: 500, 
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      });
    }

    return new Response("Ayesha Backend is Live", { headers: corsHeaders });
  }
};
          
