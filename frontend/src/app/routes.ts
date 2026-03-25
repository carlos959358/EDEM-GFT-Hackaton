import { createBrowserRouter } from 'react-router';
import { LoginScreen } from './components/LoginScreen';
import { DashboardScreen } from './components/DashboardScreen';
import { CalendarScreen } from './components/CalendarScreen';
import { RoomBookingScreen } from './components/RoomBookingScreen';
import { ChatScreen } from './components/ChatScreen';
import { ProfileScreen } from './components/ProfileScreen';
import { TasksScreen } from './components/TasksScreen';
import { SettingsScreen } from './components/SettingsScreen';
import { GradesScreen } from './components/GradesScreen';
import { AttendanceScreen } from './components/AttendanceScreen';
import { Layout } from './components/Layout';

export const router = createBrowserRouter([
  {
    path: '/',
    Component: LoginScreen,
  },
  {
    path: '/',
    Component: Layout,
    children: [
      {
        path: 'dashboard',
        Component: DashboardScreen,
      },
      {
        path: 'calendar',
        Component: CalendarScreen,
      },
      {
        path: 'rooms',
        Component: RoomBookingScreen,
      },
      {
        path: 'chat',
        Component: ChatScreen,
      },
      {
        path: 'profile',
        Component: ProfileScreen,
      },
      {
        path: 'tasks',
        Component: TasksScreen,
      },
      {
        path: 'settings',
        Component: SettingsScreen,
      },
      {
        path: 'grades',
        Component: GradesScreen,
      },
      {
        path: 'attendance',
        Component: AttendanceScreen,
      },
    ],
  },
]);
