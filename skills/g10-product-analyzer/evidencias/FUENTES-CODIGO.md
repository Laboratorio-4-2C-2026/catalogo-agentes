# Fuentes verificadas en el código de Conexia

Consulta de solo lectura del 10/11/2026. Son extractos del checkout local; no acreditan por sí solos el estado del despliegue. Se conservan ruta, líneas y hash del archivo completo.

## frontend/src/pages/trips/index.tsx

SHA-256: dbab1030b0d8b4ec45c5fd404e749000045ff58c06e9595e1953a55fd32d69db

Líneas 56–80:

~~~

56:     // Si el usuario cambia de pestaña antes de que termine el pedido, se
57:     // ignora la respuesta vieja
58:     let ignore = false;
59:
60:     Promise.all([
61:       getMyTrips(scope),
62:       scope === 'upcoming'
63:         ? getMyTravelIntents()
64:         : Promise.resolve<TravelIntent[]>([]),
65:       getProfile(),
66:     ])
67:       .then(([tripsData, intentsData, profile]) => {
68:         if (ignore) return;
69:         setTrips(tripsData);
70:         setIntents(intentsData.filter((intent) => intent.status === 'ACTIVE'));
71:         setHasCar(Boolean(profile?.hasCar));
72:         setStatus('ready');
73:       })
74:       .catch((error) => {
75:         if (ignore) return;
76:         console.error('Error al cargar los viajes:', error);
77:         setStatus('error');
78:       });
79:
80:     return () => {

~~~

## frontend/src/pages/trips/index.tsx

SHA-256: dbab1030b0d8b4ec45c5fd404e749000045ff58c06e9595e1953a55fd32d69db

Líneas 155–170:

~~~

155:             onPublish={() => setIsDrawerOpen(true)}
156:           />
157:
158:           {!isHistory && intents.length > 0 && (
159:             <section className="trips__list-section">
160:               <h2 className="trips__section-title">Mis intenciones de viaje</h2>
161:               <ul className="trips__list">
162:                 {intents.map((intent) => (
163:                   <li key={intent.id}>
164:                     <TravelIntentCard intent={intent} />
165:                   </li>
166:                 ))}
167:               </ul>
168:             </section>
169:           )}
170:

~~~

## frontend/src/lib/travelIntentsApi.ts

SHA-256: edb6a1890951523b44a5b95dacfb82d3e551c19e1b1e8371a89e9958959f1a99

Líneas 27–61:

~~~

27:
28: export async function createTravelIntent(
29:   payload: CreateTravelIntentPayload,
30: ): Promise<TravelIntent> {
31:   const response = await authFetch('/travel-intents', {
32:     method: 'POST',
33:     body: JSON.stringify(payload),
34:   });
35:
36:   if (!response.ok) {
37:     throw new Error(
38:       await getErrorMessage(
39:         response,
40:         'No pudimos publicar tu intención de viaje',
41:       ),
42:     );
43:   }
44:
45:   return response.json();
46: }
47:
48: export async function getMyTravelIntents(): Promise<TravelIntent[]> {
49:   const response = await authFetch('/travel-intents');
50:
51:   if (!response.ok) {
52:     throw new Error(
53:       await getErrorMessage(
54:         response,
55:         'No pudimos cargar tus intenciones de viaje',
56:       ),
57:     );
58:   }
59:
60:   return response.json();
61: }

~~~

## backend/src/travel-intents/travel-intents.controller.ts

SHA-256: 548ce52df65ab949364f6ed09506b3b5d6bd65d7f440c31d0b1d4e4aa59998a1

Líneas 15–35:

~~~

15:
16: @Controller('travel-intents')
17: @UseGuards(FirebaseAuthGuard)
18: export class TravelIntentsController {
19:   constructor(private readonly travelIntentsService: TravelIntentsService) {}
20:
21:   @Post()
22:   create(
23:     @CurrentUser() user: AuthenticatedUser,
24:     @Body() dto: CreateTravelIntentDto,
25:   ) {
26:     return this.travelIntentsService.create(user.id, dto);
27:   }
28:
29:   @Get()
30:   findMine(@CurrentUser() user: AuthenticatedUser) {
31:     return this.travelIntentsService.findMine(user.id);
32:   }
33:
34:   @Patch(':id/cancel')
35:   cancel(@CurrentUser() user: AuthenticatedUser, @Param('id') id: string) {

~~~

## backend/prisma/schema.prisma

SHA-256: 9ee2c2c013d8283090373e3738de01086f238bc7605d39baaa3ab42e1d9e0f70

Líneas 119–135:

~~~

119: model TripPassenger {
120:   id        String   @id @default(uuid())
121:   tripId    String
122:   userId    String
123:   pickupAddress  String?
124:   pickupLat      Float?
125:   pickupLng      Float?
126:   dropoffAddress String?
127:   dropoffLat     Float?
128:   dropoffLng     Float?
129:   createdAt DateTime @default(now())
130:
131:   trip Trip @relation(fields: [tripId], references: [id], onDelete: Cascade)
132:   user User @relation(fields: [userId], references: [id])
133:
134:   @@unique([tripId, userId])
135: }

~~~

## backend/src/travel-matches/travel-matches.service.ts

SHA-256: 7c81e0a2397deccf1b11d6c42d7fe6b7c8d241a7605c6d3847ed0fbd617e2b23

Líneas 153–171:

~~~

153:           }
154:
155:           const passenger = await addPassenger(tx, match.tripId, userId);
156:
157:           // La ubicación se copia: si la intención se cancela o vence después,
158:           // el viaje conserva dónde recoger y dejar al pasajero
159:           await tx.tripPassenger.update({
160:             where: { id: passenger.id },
161:             data: {
162:               pickupAddress: match.travelIntent.origin,
163:               pickupLat: match.travelIntent.originLat,
164:               pickupLng: match.travelIntent.originLng,
165:               dropoffAddress: match.travelIntent.destination,
166:               dropoffLat: match.travelIntent.destinationLat,
167:               dropoffLng: match.travelIntent.destinationLng,
168:             },
169:           });
170:           await tx.travelIntent.update({
171:             where: { id: match.travelIntentId },

~~~

## frontend/src/pages/tripDetails/index.tsx

SHA-256: 703fb37b12afe10c92e03be6e7604e474db08b13c35e7b4b6bbbf10641544d0c

Líneas 30–45:

~~~

30: type ParticipationAction = 'join' | 'leave';
31:
32: function getSeatsLabel(availableSeats: number): string {
33:   if (availableSeats <= 0) return 'Sin lugares libres';
34:   return `${formatSeats(availableSeats)} ${availableSeats === 1 ? 'libre' : 'libres'}`;
35: }
36:
37: function getPassengerLocation(passenger: TripPassenger): string | null {
38:   const parts = [
39:     passenger.pickupAddress && `Recoge en ${passenger.pickupAddress}`,
40:     passenger.dropoffAddress && `Deja en ${passenger.dropoffAddress}`,
41:   ].filter(Boolean);
42:
43:   return parts.length > 0 ? parts.join(' · ') : null;
44: }
45:

~~~
