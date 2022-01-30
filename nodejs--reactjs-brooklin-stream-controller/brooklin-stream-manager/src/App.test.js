import { render, screen } from '@testing-library/react';
import App from './App';

test('renders stream table', () => {
  render(<App />);
  const linkElement = screen.getByText(/stream/i);
  expect(linkElement).toBeInTheDocument();
});
