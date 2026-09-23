import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface MapComplaint { id: number; title: string; latitude: number; longitude: number; priority: string | null; status: string; }

export const ComplaintMap: React.FC<{ complaints: MapComplaint[]; height?: string }> = ({ complaints, height = "420px" }) => {
  const center: [number, number] = complaints.length
    ? [complaints[0].latitude, complaints[0].longitude]
    : [17.385, 78.4867];

  return (
    <div style={{ height }} className="rounded-lg overflow-hidden border border-slate-200">
      <MapContainer center={center} zoom={12} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {complaints.map((c) => (
          <Marker key={c.id} position={[c.latitude, c.longitude]}>
            <Popup>
              <p className="font-medium">{c.title}</p>
              <p className="text-xs">Priority: {c.priority || "N/A"}</p>
              <p className="text-xs">Status: {c.status}</p>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};
