# Fuentes verificadas en el código de Conexia

Consulta de solo lectura del 10/11/2026. Son extractos del checkout local; no acreditan por sí solos el estado del despliegue. Se conservan ruta, líneas y hash del archivo completo.

## backend/src/geo/geo.service.ts

SHA-256: 812e49b77b3780862d977af9352cd4338ec7a2cc061d5cfe1cc9a1b94ea5c193

Líneas 1–14:

~~~

1: export interface Coordinates {
2:   lat: number;
3:   lng: number;
4: }
5:
6: // Abstracción del proveedor de geolocalización. La lógica de dominio depende
7: // solo de esta clase; la implementación concreta se elige en GeoModule.
8: export abstract class GeoService {
9:   /** Devuelve null si la dirección no se puede resolver. */
10:   abstract geocode(address: string): Promise<Coordinates | null>;
11:
12:   /** Distancia en km recorriendo los puntos en orden (mínimo 2). Null si no hay ruta. */
13:   abstract getRouteDistanceKm(points: Coordinates[]): Promise<number | null>;
14: }

~~~

## backend/src/geo/geo.module.ts

SHA-256: 8b73394fc1ca7220df2777f8a5995809a49a8915ccf0d138675446b336ad155b

Líneas 1–10:

~~~

1: import { Module } from '@nestjs/common';
2: import { GeoService } from './geo.service';
3: import { GeoapifyGeoService } from './geoapify-geo.service';
4:
5: @Module({
6:   // Para cambiar de proveedor alcanza con reemplazar useClass
7:   providers: [{ provide: GeoService, useClass: GeoapifyGeoService }],
8:   exports: [GeoService],
9: })
10: export class GeoModule {}

~~~

## backend/src/geo/geoapify-geo.service.ts

SHA-256: 41e7fe2261e5d5e54c0deb02269ddee5929088fe8bb3a9076ac278e18ff0cba2

Líneas 1–62:

~~~

1: import { Injectable, ServiceUnavailableException } from '@nestjs/common';
2: import { ConfigService } from '@nestjs/config';
3: import { Coordinates, GeoService } from './geo.service';
4:
5: const GEOCODING_URL = 'https://api.geoapify.com/v1/geocode/search';
6: const ROUTING_URL = 'https://api.geoapify.com/v1/routing';
7:
8: // Geoapify casi siempre devuelve algún resultado, aunque la dirección no
9: // exista; por debajo de esta confianza se considera no resuelta
10: const MIN_CONFIDENCE = 0.5;
11:
12: interface GeocodingResponse {
13:   results?: { lat: number; lon: number; rank?: { confidence?: number } }[];
14: }
15:
16: interface RoutingResponse {
17:   features?: { properties?: { distance?: number } }[];
18: }
19:
20: @Injectable()
21: export class GeoapifyGeoService extends GeoService {
22:   private readonly apiKey: string;
23:
24:   constructor(config: ConfigService) {
25:     super();
26:     this.apiKey = config.getOrThrow<string>('GEOAPIFY_API_KEY');
27:   }
28:
29:   async geocode(address: string): Promise<Coordinates | null> {
30:     const url = new URL(GEOCODING_URL);
31:     url.searchParams.set('text', address);
32:     url.searchParams.set('filter', 'countrycode:ar');
33:     url.searchParams.set('format', 'json');
34:     url.searchParams.set('limit', '1');
35:     url.searchParams.set('apiKey', this.apiKey);
36:
37:     const response = await fetch(url);
38:     if (!response.ok) {
39:       throw new ServiceUnavailableException(
40:         'No pudimos validar la dirección, intentá más tarde',
41:       );
42:     }
43:
44:     const body = (await response.json()) as GeocodingResponse;
45:     const result = body.results?.[0];
46:     if (!result || (result.rank?.confidence ?? 0) < MIN_CONFIDENCE) {
47:       return null;
48:     }
49:     return { lat: result.lat, lng: result.lon };
50:   }
51:
52:   async getRouteDistanceKm(points: Coordinates[]): Promise<number | null> {
53:     if (points.length < 2) {
54:       throw new Error(
55:         'Se necesitan al menos dos puntos para calcular una ruta',
56:       );
57:     }
58:
59:     const url = new URL(ROUTING_URL);
60:     url.searchParams.set(
61:       'waypoints',
62:       points.map(({ lat, lng }) => `${lat},${lng}`).join('|'),

~~~
