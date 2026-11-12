// Verifica que la configuración de producción sea coherente con lo que hay
// on-chain, y escribe el resultado como JSON por stdout.
//
// Lo corre eureka-post-deploy.yml después de cada deploy, con las variables de
// producción bajadas de Vercel. Extiende lo que hace checkSigner.mjs (EP-51)
// a todo lo que, si queda mal configurado, rompe el registro sin que nada falle
// a la vista: el signer, el proxy, la pausa, el Marketplace y el bloque de
// deploy.
//
// No usa ningún secreto: solo variables públicas y lecturas de la cadena. El
// signer se compara contra EUREKA_SIGNER_ADDRESS, que tiene que ser la dirección
// de la cuenta signer de Openfort; consultarla en Openfort pediría la API key.
//
// La salida la lee un agente, así que solo lleva datos públicos, y los textos
// salen de la lista cerrada de postDeployMessages.mjs.
//
// Uso: node scripts/postDeployCheck.mjs [--env-file <ruta>] > post-deploy.json

import * as dotenv from "dotenv";
import { existsSync } from "node:fs";
import { createPublicClient, getAddress, http, isAddress } from "viem";
import { avalancheFuji } from "viem/chains";
import { TITULOS, detalle } from "./postDeployMessages.mjs";

const envFileIndex = process.argv.indexOf("--env-file");
if (envFileIndex !== -1) {
  dotenv.config({ path: process.argv[envFileIndex + 1], quiet: true });
} else {
  dotenv.config({ path: ".env.local", quiet: true });
  dotenv.config({ quiet: true });
}

// ERC-1967: bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1)
const IMPLEMENTATION_SLOT =
  "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc";

const REGISTRY_ABI = [
  { type: "function", name: "eurekaSignerAddress", stateMutability: "view", inputs: [], outputs: [{ type: "address" }] },
  { type: "function", name: "eurekaMarketplace", stateMutability: "view", inputs: [], outputs: [{ type: "address" }] },
  { type: "function", name: "paused", stateMutability: "view", inputs: [], outputs: [{ type: "bool" }] },
];

const MARKETPLACE_ABI = [
  { type: "function", name: "registry", stateMutability: "view", inputs: [], outputs: [{ type: "address" }] },
];

// Si el deploy ya incluye el minteo desde el backend (EP-58), el signer
// on-chain tiene que ser la cuenta signer de Openfort: si no, cada registro
// paga la subida a Arweave y después revierte con InvalidSignature. Antes de
// EP-58 que no coincidan es lo esperado (EP-40/EP-42), y solo es un aviso.
const DEPLOY_MINTEA = existsSync("app/api/mint/execute/route.ts");

const client = createPublicClient({
  chain: avalancheFuji,
  transport: http(process.env.RPC_URL || undefined),
});

const chequeos = [];

function registrar(id, estado, codigo, datos = {}, error = undefined) {
  chequeos.push({ id, titulo: TITULOS[id], estado, codigo, detalle: detalle(codigo, error), datos });
}

function tipoDeError(error) {
  if (!error || typeof error !== "object") return "Error";
  const nombre = /^[A-Za-z]{1,60}$/.test(error.name ?? "") ? error.name : "Error";
  const status = error.status ?? error.statusCode ?? error.response?.status;
  return /^\d{3}$/.test(String(status ?? "")) ? `${nombre} (HTTP ${status})` : nombre;
}

function normalizar(address) {
  return address && isAddress(address) ? getAddress(address) : null;
}

function iguales(a, b) {
  return a !== null && b !== null && a.toLowerCase() === b.toLowerCase();
}

async function main() {
  const registryEnv = process.env.NEXT_PUBLIC_PATENT_REGISTRY_ADDRESS ?? null;
  const registry = normalizar(registryEnv);

  // --- Registry ---------------------------------------------------------------
  let registryOk = false;
  if (!registry) {
    registrar("registry_configurado", "error", registryEnv ? "registry_invalido" : "registry_sin_definir");
  } else {
    try {
      const code = await client.getCode({ address: registry });
      registryOk = Boolean(code && code !== "0x");
      registrar("registry_configurado", registryOk ? "ok" : "error",
        registryOk ? "registry_con_contrato" : "registry_sin_contrato", { registry });
    } catch (error) {
      registrar("registry_configurado", "no_verificable", "registry_error_red", { registry }, tipoDeError(error));
    }
  }

  if (!registryOk) {
    for (const id of ["registry_es_proxy", "registry_pausado", "signer", "marketplace"]) {
      registrar(id, "no_verificable", "depende_del_registry");
    }
  } else {
    // --- Proxy ----------------------------------------------------------------
    try {
      const slot = await client.getStorageAt({ address: registry, slot: IMPLEMENTATION_SLOT });
      const esProxy = BigInt(slot ?? "0x0") !== 0n;
      const implementation = esProxy ? normalizar(`0x${slot.slice(-40)}`) : null;
      registrar("registry_es_proxy", esProxy ? "ok" : "aviso", esProxy ? "proxy_si" : "proxy_no",
        esProxy ? { implementation } : {});
    } catch (error) {
      registrar("registry_es_proxy", "no_verificable", "proxy_error", {}, tipoDeError(error));
    }

    // --- Pausa ----------------------------------------------------------------
    try {
      const pausado = await client.readContract({ address: registry, abi: REGISTRY_ABI, functionName: "paused" });
      registrar("registry_pausado", pausado ? "error" : "ok", pausado ? "pausado_si" : "pausado_no", { pausado });
    } catch (error) {
      registrar("registry_pausado", "no_verificable", "pausado_error", {}, tipoDeError(error));
    }

    // --- Signer ---------------------------------------------------------------
    const gravedad = DEPLOY_MINTEA ? "error" : "aviso";
    try {
      const signerOnChain = normalizar(
        await client.readContract({ address: registry, abi: REGISTRY_ABI, functionName: "eurekaSignerAddress" }),
      );
      const signerEsperado = normalizar(process.env.EUREKA_SIGNER_ADDRESS ?? null);
      const datos = { signer_on_chain: signerOnChain, signer_esperado: signerEsperado, deploy_mintea: DEPLOY_MINTEA };
      if (!signerEsperado) {
        registrar("signer", gravedad, "signer_sin_definir", datos);
      } else if (iguales(signerEsperado, signerOnChain)) {
        registrar("signer", "ok", "signer_coincide", datos);
      } else {
        registrar("signer", gravedad,
          DEPLOY_MINTEA ? "signer_no_coincide_mintea" : "signer_no_coincide_previo", datos);
      }
    } catch (error) {
      registrar("signer", "no_verificable", "signer_error", {}, tipoDeError(error));
    }

    // --- Marketplace ----------------------------------------------------------
    const marketplace = normalizar(process.env.NEXT_PUBLIC_PATENT_MARKETPLACE_ADDRESS ?? null);
    if (!marketplace) {
      registrar("marketplace", "aviso", "marketplace_sin_definir");
    } else {
      try {
        const deRegistry = normalizar(
          await client.readContract({ address: registry, abi: REGISTRY_ABI, functionName: "eurekaMarketplace" }),
        );
        const deMarketplace = normalizar(
          await client.readContract({ address: marketplace, abi: MARKETPLACE_ABI, functionName: "registry" }),
        );
        const ok = iguales(deRegistry, marketplace) && iguales(deMarketplace, registry);
        registrar("marketplace", ok ? "ok" : "error", ok ? "marketplace_ok" : "marketplace_no", {
          marketplace_env: marketplace,
          marketplace_del_registry: deRegistry,
          registry_del_marketplace: deMarketplace,
        });
      } catch (error) {
        registrar("marketplace", "no_verificable", "marketplace_error", { marketplace_env: marketplace },
          tipoDeError(error));
      }
    }
  }

  // --- Bloque de deploy -------------------------------------------------------
  // patentRegistryReader.ts tira "ERROR CRÍTICO" si falta, y si es posterior al
  // deploy real la reconciliación no encuentra los eventos de mint.
  const deployBlockRaw = process.env.PATENT_REGISTRY_DEPLOY_BLOCK ?? null;
  if (!deployBlockRaw || !/^\d+$/.test(deployBlockRaw)) {
    registrar("deploy_block", "error", deployBlockRaw ? "deploy_block_no_numero" : "deploy_block_sin_definir");
  } else {
    try {
      const actual = await client.getBlockNumber();
      const ok = BigInt(deployBlockRaw) <= actual;
      registrar("deploy_block", ok ? "ok" : "error", ok ? "deploy_block_ok" : "deploy_block_futuro",
        { deploy_block: deployBlockRaw, bloque_actual: actual.toString() });
    } catch (error) {
      registrar("deploy_block", "no_verificable", "deploy_block_error", { deploy_block: deployBlockRaw },
        tipoDeError(error));
    }
  }

  const contar = (estado) => chequeos.filter((c) => c.estado === estado).length;
  const salida = {
    generado: new Date().toISOString(),
    red: "avalanche-fuji",
    commit: process.env.DEPLOY_SHA ?? null,
    deploy_mintea: DEPLOY_MINTEA,
    resumen: {
      ok: contar("ok"),
      avisos: contar("aviso"),
      errores: contar("error"),
      no_verificables: contar("no_verificable"),
    },
    chequeos,
  };
  process.stdout.write(`${JSON.stringify(salida, null, 2)}\n`);
}

main().catch((error) => {
  console.error(`postDeployCheck: ${tipoDeError(error)}`);
  process.exitCode = 1;
});
