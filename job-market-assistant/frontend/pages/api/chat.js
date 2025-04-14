import axios from 'axios';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const { message, userId } = req.body;
    
    // Call our backend service
    const response = await axios.post('http://localhost:8000/chat', {
      message,
      user_id: userId
    });
    
    res.status(200).json(response.data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ message: 'Error processing your request' });
  }
}