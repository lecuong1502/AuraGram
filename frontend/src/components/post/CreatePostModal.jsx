// frontend/src/components/post/CreatePostModal.jsx
import { useState, useRef } from "react";
import { useUiStore } from "@/store/uiStore";
import { useCreatePost } from "@/hooks/usePosts";
import Modal from "@/components/common/Modal";
import Button from "@/components/common/Button";
import styles from "./CreatePostModal.module.css";

export default function CreatePostModal() {
    const isOpen = useUiStore((s) => s.uploadModalOpen);
    const closeModal = useUiStore((s) => s.closeUploadModal);
    const addToast = useUiStore((s) => s.addToast);

    const [caption, setCaption] = useState("");
    const [previews, setPreviews] = useState([]);
    const [files, setFiles] = useState([]);
    const fileRef = useRef();
    const createPost = useCreatePost();

    const handleFiles = (e) => {
        const selected = Array.from(e.target.files).slice(0, 10);
        setFiles(selected);
        setPreviews(selected.map((f) => URL.createObjectURL(f)));
    };

    const handleSubmit = async () => {
        if (!files.length) return;
        try {
            await createPost.mutateAsync({ caption, files });
            addToast("Post shared!", "success");
            handleClose();
        } catch {
            addToast("Failed to create post", "error");
        }
    };

    const handleClose = () => {
        setCaption(""); setFiles([]); setPreviews([]);
        closeModal();
    };

    return (
        <Modal isOpen={isOpen} onClose={handleClose} title="New Post">
            <div className={styles.body}>
                {previews.length === 0 ? (
                    <button className={styles.dropzone} onClick={() => fileRef.current.click()}>
                        <span className={styles.uploadIcon}>🖼</span>
                        <p>Click to select photos (up to 10)</p>
                        <input ref={fileRef} type="file" accept="image/*" multiple hidden onChange={handleFiles} />
                    </button>
                ) : (
                    <div className={styles.previews}>
                        {previews.map((src, i) => (
                            <img key={i} src={src} alt="" className={styles.preview} />
                        ))}
                    </div>
                )}

                <textarea
                    className={styles.caption}
                    placeholder="Write a caption..."
                    maxLength={2200}
                    value={caption}
                    onChange={(e) => setCaption(e.target.value)}
                />
                <span className={styles.charCount}>{caption.length}/2200</span>

                <Button
                    fullWidth
                    onClick={handleSubmit}
                    loading={createPost.isPending}
                    disabled={!files.length}
                >
                    Share
                </Button>
            </div>
        </Modal>
    );
}