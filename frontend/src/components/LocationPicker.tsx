import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";
import { LocateFixed } from "lucide-react";

// Fix default marker icon paths (Leaflet + bundlers issue)
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface Props {
  latitude: number;
  longitude: number;
  onChange: (lat: number, lon: number) => void;
  height?: string;
}

const ClickHandler: React.FC<{ onChange: (lat: number, lon: number) => void }> = ({ onChange }) => {
  useMapEvents({
    click(e) {
      onChange(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
};

export const LocationPicker: React.FC<Props> = ({ latitude, longitude, onChange, height = "300px" }) => {
  const [center, setCenter] = useState<[number, number]>([latitude, longitude]);

  useEffect(() => {
    setCenter([latitude, longitude]);
  }, [latitude, longitude]);

  const useBrowserLocation = () => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition((pos) => {
      onChange(pos.coords.latitude, pos.coords.longitude);
    });
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <p className="text-xs text-slate-500">Click on the map to set the exact location, or use your current location.</p>
        <button type="button" onClick={useBrowserLocation} className="btn-secondary text-xs py-1 px-2">
          <LocateFixed className="w-3.5 h-3.5" /> Use my location
        </button>
      </div>
      <div style={{ height }} className="rounded-lg overflow-hidden border border-slate-200">
        <MapContainer center={center} zoom={14} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={[latitude, longitude]} />
          <ClickHandler onChange={onChange} />
        </MapContainer>
      </div>
      <p className="text-xs text-slate-400 mt-1">Lat: {latitude.toFixed(5)}, Lon: {longitude.toFixed(5)}</p>
    </div>
  );
};
