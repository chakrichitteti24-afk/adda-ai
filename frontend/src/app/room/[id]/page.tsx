import RoomClient from './RoomClient';

export async function generateStaticParams() {
  return [{ id: 'default' }];
}

export default function RoomPage() {
  return <RoomClient />;
}
