import cv2
import time
import argparse
import torch
from ultralytics import RTDETR
from collections import deque, Counter

# Import modul buatan sendiri
from config import get_next_record_folder, CLASS_MEDIUM
from visualizer import draw_luxury_box
from logic import FatigueStateMachine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="/Dataset/best.pt")
    parser.add_argument("--conf", type=float, default=0.5)
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--webcam", type=int, default=0)
    args = parser.parse_args()

    DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = RTDETR(args.model)
    
    output_folder = get_next_record_folder()
    video_path = os.path.join(output_folder, "deteksi_video.mp4")
    
    cap = cv2.VideoCapture(args.webcam)
    w, h = int(cap.get(3)), int(cap.get(4))
    video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), 30, (w, h))

    # Inisialisasi Logika
    state_machine = FatigueStateMachine(force_duration=2.0)
    class_buffer = deque(maxlen=5)
    registered_classes = set()
    class_order = {}
    order_to_name = {}
    
    stable_tracker = {"class": None, "start": 0}
    prev_time = time.time()

    print(f"System Ready. Saving to: {output_folder}")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            now = time.time()

            results = model.predict(frame, conf=args.conf, iou=args.iou, device=DEVICE, verbose=False)
            result = results[0]
            
            # 1. Klasifikasi & Smoothing
            smoothed_class = None
            if result.boxes:
                confs = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy().astype(int)
                detected = model.names[classes[confs.argmax()]]
                class_buffer.append(detected)
                
                if len(class_buffer) == 5:
                    smoothed_class = Counter(class_buffer).most_common(1)[0][0]

            # 2. Form Input Check
            if smoothed_class:
                if stable_tracker["class"] != smoothed_class:
                    stable_tracker = {"class": smoothed_class, "start": now}
                elif now - stable_tracker["start"] >= 0.5 and smoothed_class not in registered_classes:
                    print(f"\n[!] DAFTARKAN KELAS: {smoothed_class}")
                    order = input("   > Urutan (1:Normal, 2:Sedang, 3:Berat): ")
                    if order in ["1", "2", "3"]:
                        val = int(order)
                        class_order[smoothed_class] = val
                        order_to_name[val] = smoothed_class
                        registered_classes.add(smoothed_class)

            # 3. Update State Logic
            current_state = state_machine.update(smoothed_class, class_order, order_to_name)

            # 4. Rendering
            annotated = frame.copy()
            if result.boxes:
                box = result.boxes.xyxy[confs.argmax()].cpu().numpy()
                label = current_state if current_state in registered_classes else "Detecting..."
                
                # Tentukan warna
                ord_val = class_order.get(label, 0)
                color = (0, 255, 0) if ord_val == 1 else (0, 165, 255) if ord_val == 2 else (0, 0, 255)
                
                annotated = draw_luxury_box(annotated, box, label, color)

            # Dashboard Info
            fps = int(1 / (time.time() - prev_time + 1e-6))
            prev_time = time.time()
            cv2.putText(annotated, f"FPS: {fps} | State: {current_state}", (10, 30), 1, 1.5, (0, 255, 255), 2)

            cv2.imshow("RT-DETR Fatigue System", annotated)
            video_writer.write(annotated)

            if cv2.waitKey(1) & 0xFF == ord('q'): break
    finally:
        cap.release()
        video_writer.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import os
    main()