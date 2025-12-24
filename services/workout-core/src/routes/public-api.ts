import { Router, Request, Response } from 'express';

const router = Router();

router.post('get-user-data', (req: Request, res: Response) => {
  
});

/* ToDo: Make those commented endpoints in Backend API using gRPC. 
router.post('create-user', (req: Request, res: Response) => {
});

router.post('delete-user', (req: Request, res: Response) => {
});
*/

router.post('add-workout', (req: Request, res: Response) => {
  
});

router.post('update-workout', (req: Request, res: Response) => {
  
});

router.post('delete-workout', (req: Request, res: Response) => {
  
});



export default router;