import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://brnkzzyobciuufbsbxrw.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJybmt6enlvYmNpdXVmYnNieHJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc3NjA5NzksImV4cCI6MjA5MzMzNjk3OX0.9LHpNjtuXa6s8r4wETbtLpKAHsbvvJip9UZd2NMCucw'

const supabase = createClient(supabaseUrl, supabaseKey)

async function obtenerEstudiante() {
  const { data, error } = await supabase
    .from('Estudiante')
    .select('*')

  if (error) {
    console.log('Error:', error)
  } else {
    console.log('Datos:', data)
  }
}

obtenerEstudiante()