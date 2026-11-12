// Los únicos textos que puede producir postDeployCheck.mjs.
//
// Es una lista cerrada a propósito: validatePostDeploy.mjs rechaza cualquier
// título o detalle que no salga de acá, así que nada que no esté escrito en
// este archivo puede llegar al agente ni a un issue. `{error}` es el único
// hueco, y solo admite el tipo de un error (ver ERROR_TIPO).

export const TITULOS = {
  registry_configurado: "Dirección del Registry",
  registry_es_proxy: "Proxy ERC-1967",
  registry_pausado: "Registry pausado",
  signer: "Signer on-chain vs. EUREKA_SIGNER_ADDRESS",
  marketplace: "Vínculo Registry / Marketplace",
  deploy_block: "PATENT_REGISTRY_DEPLOY_BLOCK",
};

export const DETALLES = {
  registry_invalido: "NEXT_PUBLIC_PATENT_REGISTRY_ADDRESS no es una dirección válida.",
  registry_sin_definir: "NEXT_PUBLIC_PATENT_REGISTRY_ADDRESS no está definida en producción.",
  registry_con_contrato: "Hay un contrato desplegado en la dirección configurada.",
  registry_sin_contrato: "No hay ningún contrato en la dirección configurada en Fuji.",
  registry_error_red: "No se pudo consultar la red: {error}.",
  depende_del_registry: "Depende de que el Registry esté bien configurado.",
  proxy_si: "El Registry es un proxy actualizable.",
  proxy_no: "El Registry no es un proxy: los upgrades de EP-35 no aplican a esta dirección.",
  proxy_error: "No se pudo leer el slot de implementación: {error}.",
  pausado_si: "El Registry está pausado: todo registro revierte con EnforcedPause.",
  pausado_no: "El Registry no está pausado.",
  pausado_error: "No se pudo leer paused(): {error}.",
  signer_error: "No se pudo leer eurekaSignerAddress(): {error}.",
  signer_sin_definir:
    "EUREKA_SIGNER_ADDRESS no está definida en producción: no hay contra qué comparar el signer on-chain.",
  signer_coincide:
    "El contrato acepta las firmas de la dirección configurada como signer.",
  signer_no_coincide_mintea:
    "El contrato no acepta las firmas del backend: cada registro sube a Arweave y después revierte con InvalidSignature. Falta setSigner en el Registry, o EUREKA_SIGNER_ADDRESS no es la cuenta signer de Openfort.",
  signer_no_coincide_previo:
    "No coinciden, pero este deploy todavía no mintea desde el backend.",
  marketplace_sin_definir:
    "NEXT_PUBLIC_PATENT_MARKETPLACE_ADDRESS no está definida o no es válida.",
  marketplace_ok: "El Registry y el Marketplace configurados se apuntan entre sí.",
  marketplace_no:
    "El Registry y el Marketplace configurados no se apuntan entre sí: las compras y transferencias van a revertir.",
  marketplace_error: "No se pudo leer el vínculo: {error}.",
  deploy_block_no_numero: "No es un número de bloque.",
  deploy_block_sin_definir:
    "No está definida en producción: la lectura de eventos del Registry falla.",
  deploy_block_ok: "El bloque de deploy es anterior al bloque actual.",
  deploy_block_futuro: "El bloque de deploy es posterior al bloque actual de Fuji.",
  deploy_block_error: "No se pudo leer el bloque actual: {error}.",
};

// Lo único que puede ir en `{error}`: el nombre de la clase y, si lo hay, el
// status HTTP. Nunca el mensaje, que puede arrastrar una URL con API key.
export const ERROR_TIPO = /^[A-Za-z]{1,60}( \(HTTP \d{3}\))?$/;

export function detalle(codigo, error) {
  const plantilla = DETALLES[codigo];
  if (!plantilla) throw new Error(`código de detalle desconocido: ${codigo}`);
  return error === undefined ? plantilla : plantilla.replace("{error}", error);
}
