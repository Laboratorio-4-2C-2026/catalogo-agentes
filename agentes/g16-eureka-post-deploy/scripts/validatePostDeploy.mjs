// Valida post-deploy.json antes de que salga del job que lo produjo.
//
// Corre en eureka-post-deploy.yml antes de subir el artifact: si algo no tiene
// exactamente la forma esperada, el JSON no se sube, no lo lee el agente y no
// llega a ningún issue. No es una heurística de "parece una clave": títulos y
// detalles tienen que coincidir con la lista cerrada de postDeployMessages.mjs,
// y los datos solo pueden ser direcciones, números o booleanos.
//
// Uso: node scripts/validatePostDeploy.mjs post-deploy.json
// Sale con código 0 si es válido y 1 si no, con el motivo por stderr.

import { readFileSync } from "node:fs";
import { DETALLES, ERROR_TIPO, TITULOS } from "./postDeployMessages.mjs";

const ESTADOS = ["ok", "aviso", "error", "no_verificable"];
const CLAVES_RAIZ = ["generado", "red", "commit", "deploy_mintea", "resumen", "chequeos"];
const CLAVES_CHEQUEO = ["id", "titulo", "estado", "codigo", "detalle", "datos"];
const DIRECCION = /^0x[0-9a-fA-F]{40}$/;
const NUMERO = /^\d{1,20}$/;

function detalleValido(codigo, texto) {
  const plantilla = DETALLES[codigo];
  if (typeof plantilla !== "string" || typeof texto !== "string") return false;
  if (!plantilla.includes("{error}")) return texto === plantilla;
  const [antes, despues] = plantilla.split("{error}");
  if (!texto.startsWith(antes) || !texto.endsWith(despues)) return false;
  return ERROR_TIPO.test(texto.slice(antes.length, texto.length - despues.length));
}

const datoValido = (v) =>
  v === null || typeof v === "boolean" || (typeof v === "string" && (DIRECCION.test(v) || NUMERO.test(v)));

function motivoDeRechazo(f) {
  if (!f || typeof f !== "object" || Array.isArray(f)) return "no es un objeto";
  if (!Object.keys(f).every((k) => CLAVES_RAIZ.includes(k))) return "claves de primer nivel inesperadas";
  if (typeof f.generado !== "string" || Number.isNaN(Date.parse(f.generado))) return "generado inválido";
  if (f.red !== "avalanche-fuji") return "red inesperada";
  if (f.commit !== null && !/^[0-9a-f]{40}$/.test(f.commit)) return "commit inválido";
  if (typeof f.deploy_mintea !== "boolean") return "deploy_mintea inválido";
  if (!["ok", "avisos", "errores", "no_verificables"].every((k) => Number.isInteger(f.resumen?.[k])))
    return "resumen inválido";
  if (Object.keys(f.resumen).length !== 4) return "resumen con claves de más";
  if (!Array.isArray(f.chequeos) || f.chequeos.length > Object.keys(TITULOS).length) return "chequeos inválidos";
  for (const c of f.chequeos) {
    if (!c || !Object.keys(c).every((k) => CLAVES_CHEQUEO.includes(k))) return "chequeo con claves inesperadas";
    if (!(c.id in TITULOS) || c.titulo !== TITULOS[c.id]) return "título o id fuera de la lista";
    if (!ESTADOS.includes(c.estado)) return `estado inválido en ${c.id}`;
    if (!detalleValido(c.codigo, c.detalle)) return `detalle fuera de la lista en ${c.id}`;
    if (!c.datos || typeof c.datos !== "object" || Array.isArray(c.datos)) return `datos inválidos en ${c.id}`;
    for (const [clave, valor] of Object.entries(c.datos)) {
      if (!/^[a-z_]{1,40}$/.test(clave) || !datoValido(valor)) return `dato inválido en ${c.id}`;
    }
  }
  const contados = { ok: 0, aviso: 0, error: 0, no_verificable: 0 };
  for (const c of f.chequeos) contados[c.estado] += 1;
  if (contados.ok !== f.resumen.ok || contados.aviso !== f.resumen.avisos
    || contados.error !== f.resumen.errores || contados.no_verificable !== f.resumen.no_verificables)
    return "el resumen no coincide con los chequeos";
  return null;
}

let motivo;
try {
  motivo = motivoDeRechazo(JSON.parse(readFileSync(process.argv[2], "utf8")));
} catch {
  motivo = "no se pudo leer como JSON";
}

if (motivo) {
  console.error(`post-deploy.json rechazado: ${motivo}`);
  process.exitCode = 1;
}
