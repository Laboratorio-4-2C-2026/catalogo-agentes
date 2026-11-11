// Carga los datos de la demo por la API. Asume una base recién creada.
const API = process.env.API_URL ?? 'http://localhost:8080/api/v1'
export const PASSWORD = 'Demo1234'

const USERS = {
  martina: { name: 'Martina López', email: 'martina.lopez@demo.com' },
  tomas: { name: 'Tomás Ruiz', email: 'tomas.ruiz@demo.com' },
  lucia: { name: 'Lucía Fernández', email: 'lucia.fernandez@demo.com' },
  nico: { name: 'Nicolás Pérez', email: 'nicolas.perez@demo.com' },
  sofia: { name: 'Sofía Gómez', email: 'sofia.gomez@demo.com' },
  juan: { name: 'Juan Díaz', email: 'juan.diaz@demo.com' },
}

const GROUPS = [
  {
    owner: 'martina',
    name: 'Análisis Matemático II',
    description: 'Integrales múltiples, series y ecuaciones diferenciales. Nos juntamos martes y jueves.',
    members: ['lucia', 'nico', 'sofia'],
  },
  {
    owner: 'martina',
    name: 'Bases de Datos',
    description:
      'Preparación del parcial: SQL, normalización y transacciones.\nTraer ejercicios resueltos de la guía 3.',
    members: ['sofia', 'juan'],
  },
  { owner: 'martina', name: 'Física I', description: 'Cinemática y dinámica.', members: ['nico'] },
  { owner: 'lucia', name: 'Algoritmos y Estructuras de Datos', description: null, members: ['martina', 'sofia', 'juan'] },
  { owner: 'sofia', name: 'Inglés Técnico', description: 'Lectura de papers y vocabulario.', members: ['martina'] },
  { owner: 'tomas', name: 'Programación Orientada a Objetos', description: null, members: ['juan'] },
]

async function call(method, path, body, token) {
  const response = await fetch(`${API}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  const json = await response.json().catch(() => null)
  if (!response.ok) throw new Error(`${method} ${path} -> ${response.status} ${JSON.stringify(json)}`)
  return json.data
}

export async function seed() {
  const tokens = {}
  for (const [key, user] of Object.entries(USERS)) {
    await call('POST', '/auth/register', { ...user, password: PASSWORD })
    tokens[key] = (await call('POST', '/auth/login', { email: user.email, password: PASSWORD })).token
  }

  const ids = {}
  for (const key of Object.keys(USERS)) {
    // El JWT trae el id del usuario en `sub`.
    ids[key] = JSON.parse(Buffer.from(tokens[key].split('.')[1], 'base64url').toString()).sub
  }

  for (const group of GROUPS) {
    const created = await call(
      'POST',
      '/groups',
      { name: group.name, description: group.description },
      tokens[group.owner],
    )
    for (const member of group.members) {
      await call('POST', `/groups/${created.id}/invitations`, { userId: ids[member] }, tokens[group.owner])
      const pending = await call('GET', '/invitations/me', null, tokens[member])
      const invitation = pending.find((item) => item.group.id === created.id)
      await call('PATCH', `/invitations/${invitation.id}`, { status: 'ACCEPTED' }, tokens[member])
    }
    console.log(`grupo: ${group.name} (${group.members.length + 1} miembros)`)
  }

  return USERS
}

if (import.meta.url === `file:///${process.argv[1].replaceAll('\\', '/')}`) {
  await seed()
}
