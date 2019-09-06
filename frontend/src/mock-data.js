export function getPrinciples() {
  return [
    {id: "1", name: "Adhesión voluntaria y abierta", description: `Las cooperativas son organizaciones voluntarias, abiertas
      a todas las personas capacitadas para utilizar sus servicios y dispuestas a aceptar las responsabilidades
      de ser socias, sin discriminación por motivos de sexo, raza, situación social, política o religiosa.`},
    {id: "2", name: "Gestión democrática por parte de los socios", description: `Las cooperativas son organizaciones gestionadas
      democráticamente por las personas socias, quienes participan activamente fijando sus políticas y tomando decisiones.
      Los hombres y mujeres elegidos para representar y gestionar las cooperativas son responsables ante el resto.`},
    {id: "3", name: "Participación económica de los socios", description: `Las personas socias contribuyen equitativamente al capital
      de sus cooperativas y lo gestionan de forma democrática`},
    {id: "4", name: "Autonomía e independencia", description: `Las cooperativas son organizaciones autónomas de autoayuda,
      gestionadas por las personas socias.`},
    {id: "5", name: "Educación, formación e información", description: `Las cooperativas proporcionan educación e información a las
      personas socias, a los representantes elegidos, a los cargos directivos y a los trabajadores que puedan contribuir de
      manera eficaz al desarrollo de sus cooperativas. Informan al público, especialmente a la juventud y a los líderes de opinión,
      de la naturaleza y beneficios de la cooperativa.`},
    {id: "6", name: "Cooperación entre cooperativas", description: `Las cooperativas sirven a las personas socias lo más eficazmente posible
      y fortalecen el movimiento cooperativo trabajando conjuntamente mediante estructuras locales, nacionales, regionales e internacionales.`},
    {id: "7", name: "Interés por la comunidad", description: `Las cooperativas trabajan para conseguir el desarrollo sostenible de sus comunidades
      mediante políticas aprobadas por su tejido social.`},
  ];
}

export function findPrinciple(id) {
  return getPrinciples().find((p) => {
    return p.id === id
  });
}

export function deletePrinciple(id) {
  const index = getPrinciples().findIndex((p) => {
    return p.id === id
  });
  const principles = getPrinciples();
  principles.splice(index, 1);
  return principles;
}