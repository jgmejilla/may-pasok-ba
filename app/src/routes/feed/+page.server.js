import { supabase } from "$lib/supabaseClient"

export async function load() {
    const { data } = await supabase.from("articles").select()

    return {
        articles: data ?? []
    }
}