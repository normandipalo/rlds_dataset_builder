## Dataset and Setup Information
We use a Sawyer robot with a Robotiq 2F-85 gripper. We use a RealSense D435 camera mounted on the wrist. In particular, if we consider an x-axis pointing "forward" or in front of the robot, a y-axis pointing to the left, and a z-axis pointing up, following the right-hand convention, with this reference frame having the origin on the tip of the end-effector, the camera is mounted at (7cm, 0cm, 18cm) - i.e. 18cm "up" and 7cm "forward" of the end-effector tip. The camera is parallel to the z-axis, looking straight down.

Here's a one line description of each task:

1. **grasp can**: grasp a can places horizontally on a table and lift it.
2. **hang cup**: starting with a cup in the end-effector, place it on a tree mug holder.
3. **insert cap in bottle**: starting with a bottle cap in the end-effector, insert it in an empty bottle on the table.
4. **insert toast**: starting with a toy bread slice in the end-effector, insert it in a toy toaster on the table.
5. **open bottle**: remove the cap from a bottle on a table by grasping and lifting the cap.
6. **open lid**: remove the lid from a pot on the table by grasping it and lifting it.
7. **pick up apple**: pick up an apple from the table.
8. **pick up bottle**: pick up a bottle placed horizontally on the table.
9. **pick up kettle**: pick up a toy kettle from the handle.
10. **pick up mug**: pick up a mug from the table (no need to grasp it from the handle).
11. **pick up pan**: pick up a toy pan from the table, grasping it from the handle.
12. **pick up shoe**: pick up a shoe from the table.
13. **pour in mug**: starting with a cup in the end-effector, pour into a mug on the table - success is detected by dropping a marble from the cup to the mug, mimicking a liquid.
14. **put apple in pot**: starting with an apple in the end-effector, drop in in a pot on the table.
15. **put cup in dishwasher**: starting with a cup in the end-effector, place it in an empty area of a toy dishwasher rack on the table.
16. **stack bowls**: starting with a bowl in the end-effector, stack in on top of another bowl on the table.
17. **swipe**: starting with a dust brush in the end-effector, swipe a marble into a dustpan on the table.


Here are a few example GIFs: the arrow indicates the x and y components of the action, with a red arrow indicating a closed end-effector and the blue arrow an open end-effector. The red arc indicates the amount of rotation around the z-axis, although all three axes of rotations are recorded.

![](https://github.com/normandipalo/rlds_dataset_builder/blob/main/imperial_wrist_dataset/gifs/insert_toast.gif)
![](https://github.com/normandipalo/rlds_dataset_builder/blob/main/imperial_wrist_dataset/gifs/insert_cap_in_bottle.gif)
![](https://github.com/normandipalo/rlds_dataset_builder/blob/main/imperial_wrist_dataset/gifs/pick_up_bottle.gif)
![](https://github.com/normandipalo/rlds_dataset_builder/blob/main/imperial_wrist_dataset/gifs/pick_up_mug.gif)
![](https://github.com/normandipalo/rlds_dataset_builder/blob/main/imperial_wrist_dataset/gifs/stack_bowls.gif)
