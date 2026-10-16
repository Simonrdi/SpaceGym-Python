async function initMap() {
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const map = new Map(document.getElementById("map"), {
    zoom: 13,
    center: { lat: 41.737829, lng: 12.279703 },
    mapId: "4504f8b37365c3d0",
  });

  const Palestre = [
    {
      position: { lat: 41.737829, lng: 12.279703 },
      title: "Pianeta Fitness",
    },
    {
      position: { lat: 41.740274, lng: 12.253095 },
      title: "Talento e tenacia.",
    },
    {
      position: { lat: 41.726764, lng: 12.300620 },
      title: "Heaven gym",
    },
    {
      position: { lat: 41.772055, lng: 12.355038 },
      title: "Kristall",
    },
    {
      position: { lat: 41.789462, lng: 12.404012 },
      title: "Fly-fit Gym",
    },
    {
      position: { lat: 41.771669, lng: 12.333723}, 
      title: "Il Gladiatore"
    },
    {
      position: { lat: 41.789933, lng: 12.431571},
      title: "Xcross"
    },
    {
      position: { lat: 41.864896, lng: 12.485415},
      title: "Fenix Gym ",
      
    }
  ];

  const infoWindow = new InfoWindow();


  Palestre.forEach(({ position, title }, i) => {
    const pin = new PinElement({
      
      scale: 0.8,
    });
    const marker = new AdvancedMarkerElement({
      position,
      map,
      title: `${i + 1}. ${title}`,
      content: pin.element,
      gmpClickable: true,
    });


    marker.addListener("click", ({ domEvent, latLng }) => {
      const { target } = domEvent;

      infoWindow.close();
      infoWindow.setContent(marker.title);
      infoWindow.open(marker.map, marker);
    });
  });
}

initMap();