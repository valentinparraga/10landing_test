import { faker } from '@faker-js/faker';

export const Barberos = () =>{

  function generarBarbero() {
    const locations = ['Ensenada', 'La Plata'];

    return {
      id: faker.string.uuid(), //genera un hash ID: '4136cd0b-d90b-4af7-b485-5d1ded8db252'
      name: faker.person.fullName({ sex: 'male' }),
      job: faker.number.int({ min: 2017, max: 2025 }),
      img: faker.image.personPortrait({ sex: 'male', size: '256' }),
      phone: faker.phone.number(({ style: 'national' })),
      location: locations[Math.floor(Math.random() * locations.length)],
    };
  }

  // Cambia este número por la cantidad que quieras generar
  const cantidad = 5;

  // Generar X barberos
  const barberos = Array.from({ length: cantidad }, generarBarbero);

    return <section className='w-full mb-12'>
        <div className='flex flex-wrap justify-center mx-auto p-2 gap-2'>
            {barberos.map(barb => (
              <div key={barb.id} className='bg-slate-950 border-slate-700 border-2 rounded-md text-1xl'>
                <div>
                  <img src={barb.img} alt={barb.name} />
                  <h4 className='font-semibold'>{barb.name}</h4>
                  <p className='flex flex-col'>
                    <span>{barb.phone}</span>
                    <span>Trabaja desde: {barb.job}</span>
                    <span>Sucursal: {barb.location}</span>
                  </p>
                </div>
              </div>
            ))}
        </div>
            <button>
              <p className='text-2xl'>Agendá tu turno</p>
            </button>
    </section>
}